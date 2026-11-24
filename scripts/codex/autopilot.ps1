# Codex account autopilot (ported from multisingal_accelerator nd_autopilot2.ps1).
# One queue per account; each account runs one task at a time through codex_worker.sh.
# Item = (id, task file under $spec, effort, max runs, gate). Gate '' = start now,
# 'flag:<path>' = wait for that file, 'done:<id>' = wait until that task ends ALL_PASS/GATE_FAIL.
# Usage-limited account -> retry in 30 min. Log: runs\codex\autopilot.log. Stop: kill this process.
# Edit $Q before each campaign. Launching this = user approval (sets CODEX_MANUAL_APPROVED=1).
$repo=(Resolve-Path "$PSScriptRoot\..\..").Path; $logd="$repo\runs\codex"; $reg="$logd\registry"
$spec='scripts/codex/tasks'; $model=$(if($env:CODEX_MODEL){$env:CODEX_MODEL}else{'gpt-6.1-terra'})
$bashRepo='/'+$repo.Substring(0,1).ToLower()+($repo.Substring(2) -replace '\\','/')
function L($m){ "$(Get-Date -Format o) $m" | Add-Content "$logd\autopilot.log" }
$Q=[ordered]@{
  # 'C:\Users\ADMIN\.codex-A' = @(@('t01_example','T01_EXAMPLE.md','medium',2,''))
  # 'C:\Users\ADMIN\.codex-B' = @(@('t02_after','T02_AFTER.md','medium',2,'done:t01_example'))
}
function Ended($id){ $sf="$reg\status\$id.txt"; (Test-Path $sf) -and ((Get-Content $sf | Select -Last 1) -match "end $id STATUS: (ALL_PASS|GATE_FAIL)") }
$st=@{}; foreach($a in $Q.Keys){ $st[$a]=@{i=0;run=0;cur=$null;wait=(Get-Date).AddSeconds(-1)} }
foreach($a in $Q.Keys){ for($k=0;$k -lt $Q[$a].Count;$k++){ $id=$Q[$a][$k][0]
  if(Test-Path "$reg\running\$id.lock"){ $st[$a].i=$k; $st[$a].cur=$id; $st[$a].run=1; break }
  if(Ended $id){ $st[$a].i=$k+1; continue }; break } }
function GateOpen($g){
  if(-not $g){ return $true }
  if($g -like 'flag:*'){ return (Test-Path $g.Substring(5)) }
  $id=$g.Substring(5); if(Ended $id){ return $true }
  foreach($a in $Q.Keys){ $ids=@($Q[$a] | %{ $_[0] }); $k=[array]::IndexOf($ids,$id); if($k -ge 0 -and $st[$a].i -gt $k){ return $true } }
  return $false }
function Probe($acct){ if($acct -ne 'default'){ $env:CODEX_HOME=$acct }
  $o = & codex exec -m $model -c model_reasoning_effort=low --skip-git-repo-check -C $repo "Reply with the single word OK." 2>&1 | Out-String
  Remove-Item Env:CODEX_HOME -ErrorAction SilentlyContinue; return -not ($o -match 'usage limit|not supported') }
L ('start; adopted: ' + (($st.GetEnumerator() | ?{ $_.Value.cur } | %{ $_.Value.cur }) -join ', '))
while($true){
  $alldone=$true
  foreach($a in @($Q.Keys)){
    $s=$st[$a]; if($s.i -ge $Q[$a].Count){ continue }; $alldone=$false
    if($s.cur){
      if(Test-Path "$reg\running\$($s.cur).lock"){ continue }
      $last=Get-Content "$reg\status\$($s.cur).txt" -ErrorAction SilentlyContinue | Select -Last 1
      $lf=Get-ChildItem $logd -Filter "$($s.cur)_2*.log" | Sort LastWriteTime -Desc | Select -First 1
      $limited=[bool]($lf -and (Select-String $lf.FullName -Pattern "usage limit" -Quiet))
      L "$($s.cur) ended: $last limited=$limited"; $item=$Q[$a][$s.i]; $s.cur=$null
      if($limited){ $s.wait=(Get-Date).AddMinutes(30); $s.run-- }
      elseif($last -match 'ALL_PASS|GATE_FAIL' -or $s.run -ge $item[3]){ $s.i++; $s.run=0; if($s.i -ge $Q[$a].Count){ L "queue done for $a"; continue } }
    }
    if((Get-Date) -lt $s.wait){ continue }
    $item=$Q[$a][$s.i]; if(-not (GateOpen $item[4])){ continue }
    if(-not (Probe $a)){ L "$a limited; retry in 30 min"; $s.wait=(Get-Date).AddMinutes(30); continue }
    $s.run++; $id=$item[0]; $s.cur=$id
    Remove-Item "$reg\running\$id.lock" -ErrorAction SilentlyContinue
    $cmd="cd '$bashRepo' && export CODEX_MANUAL_APPROVED=1 CODEX_ALLOW_HIGH=1 CODEX_MAX_WORKERS=$($Q.Count) && bash scripts/codex/codex_worker.sh $id '$a' $spec/$($item[1]) $model $($item[2]) > runs/codex/launch_$id.out 2>&1"
    Start-Process 'C:\Program Files\Git\bin\bash.exe' -ArgumentList '-lc',"`"$cmd`"" -WindowStyle Hidden | Out-Null
    L "launch $id on $a (run $($s.run)/$($item[3]), $($item[2]))"; Start-Sleep 30
  }
  if($alldone){ break }; Start-Sleep 120
}
L 'autopilot done'
