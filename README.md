# ecotop
A customizable GPU monitoring script


![ecotop example](https://i.imgur.com/NBFSdXn.png)

## Usage
```
   _____________  __             
  / __/ ___/ __ \/ /____  ___    
 / _// /__/ /_/ / __/ _ \/ _ \   
/___/\___/\____/\__/\___/ .__/   
                       /_/       

---HELP---
Usage: ecotop <Gauge1> [Color(s)] ... <GaugeN> [Color(s)] 
╔════════════╦════╦═════════════╗  
║Gauge       ║Arg ║Color(s)     ║  
╠════════════╬════╬═════════════╣  
┃Utilization ┃-u  ┃<color1>     ┃  
┃Temperature ┃-t  ┃<color1,2,3> ┃  
┃Fan Speed   ┃-f  ┃<color1>     ┃  
┃Power Usage ┃-p  ┃<color1>     ┃  
┃Memory      ┃-m  ┃<color1>     ┃  
┃Memory (%)  ┃-mp ┃<color1>     ┃  
┃Memory (Mb) ┃-mv ┃<color1>     ┃  
┗━━━━━━━━━━━━┻━━━━┻━━━━━━━━━━━━━┛  

-All Color Arguments are optional.
-Gauges will be desplayed in the order they are entered.

 Colors
┏━━━━━━━━┓
┃grey    ┃
┃red     ┃
┃green   ┃
┃yellow  ┃
┃blue    ┃
┃magenta ┃
┃cyan    ┃
┃white   ┃
┗━━━━━━━━┛
```
## Notes
Now works with Nvidia and AMD GPUs! 
For AMD GPUs you must use (amdgpu-fan)[https://github.com/chestm007/amdgpu-fan] for your fan control. Without it the fan speed reporting will be innacurate.

## Dependencies 
```
gpustat
termcolor
pyamdgpuinfo
amdgpu_fan
```

