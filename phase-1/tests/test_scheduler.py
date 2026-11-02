import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from citizen_os.models import ProcessState,ServiceProcess
from citizen_os.scheduler import fcfs,sjf,srtf,priority,round_robin
class SchedulerTests(unittest.TestCase):
 def setUp(self): self.jobs=[ServiceProcess(1,"A","Form A",5,0,2),ServiceProcess(2,"B","Form B",3,1,1),ServiceProcess(3,"C","Form C",1,2,3)]
 def test_fcfs_metrics(self):
  r=fcfs(self.jobs); self.assertEqual([p.completion_time for p in r.processes],[5,8,9]); self.assertEqual([p.waiting_time for p in r.processes],[0,4,6])
 def test_sjf_order(self): self.assertEqual([x[0] for x in sjf(self.jobs).timeline],[1,3,2])
 def test_priority_order(self): self.assertEqual([x[0] for x in priority(self.jobs).timeline],[1,2,3])
 def test_rr_terminates_all(self): self.assertTrue(all(p.state==ProcessState.TERMINATED for p in round_robin(self.jobs,2).processes))
 def test_srtf_preempts(self): self.assertEqual(srtf(self.jobs).processes[1].completion_time,5)
 def test_bad_quantum(self):
  with self.assertRaises(ValueError): round_robin(self.jobs,0)
 def test_empty(self):
  with self.assertRaises(ValueError): fcfs([])
if __name__=="__main__": unittest.main()
