import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from citizen_os.models import ServiceProcess,ProcessState
class ProcessModelTests(unittest.TestCase):
 def test_initial_state_and_pcb(self):
  p=ServiceProcess(10,"Test","Certificate",4); self.assertEqual(p.state,ProcessState.NEW); self.assertEqual(p.remaining_time,4); self.assertEqual(p.pcb_snapshot()["pid"],10)
 def test_invalid_burst(self):
  with self.assertRaises(ValueError): ServiceProcess(1,"A","B",0)
 def test_negative_arrival(self):
  with self.assertRaises(ValueError): ServiceProcess(1,"A","B",2,-1)
if __name__=="__main__": unittest.main()
