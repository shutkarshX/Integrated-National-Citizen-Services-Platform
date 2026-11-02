"""Read-only inspection of the actual Linux host."""
import platform, shutil, subprocess
from pathlib import Path
def _read(path):
    try: return Path(path).read_text(encoding="utf-8").strip()
    except OSError: return "Unavailable"
def collect_system_info():
    info={"operating_system":platform.system(),"release":platform.release(),"architecture":platform.machine(),"python":platform.python_version(),"hostname":platform.node(),"distribution":_read("/etc/os-release")}
    for label,cmd in (("kernel",["uname","-r"]),("uptime",["uptime","-p"]),("memory",["free","-h"]),("disk",["df","-h","/"])):
        if not shutil.which(cmd[0]): info[label]=f"{cmd[0]} not installed"; continue
        try: info[label]=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=5).stdout.strip()
        except (subprocess.SubprocessError,OSError): info[label]="Command unavailable or failed"
    return info
