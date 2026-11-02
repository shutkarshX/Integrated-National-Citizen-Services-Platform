import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from citizen_os.models import ProcessState,ServiceProcess
from citizen_os.scheduler import multilevel_queue,multilevel_feedback_queue

class MultilevelSchedulerTests(unittest.TestCase):
    def test_mlq_keeps_fixed_priority_queues_and_completes(self):
        jobs=[ServiceProcess(1,"A","General",4,0,2),ServiceProcess(2,"B","Urgent",2,1,1)]
        result=multilevel_queue(jobs,quantum=2)
        self.assertEqual(result.timeline,[(1,0,1),(2,1,3),(1,3,5),(1,5,6)])
        self.assertTrue(all(p.state==ProcessState.TERMINATED for p in result.processes))

    def test_mlq_rejects_invalid_quantum(self):
        with self.assertRaises(ValueError):
            multilevel_queue([ServiceProcess(1,"A","X",1)],0)

    def test_mlfq_demotes_long_running_process(self):
        jobs=[ServiceProcess(1,"A","Long",7,0),ServiceProcess(2,"B","Short",1,1)]
        result=multilevel_feedback_queue(jobs,quantums=(2,4,8))
        self.assertEqual(result.processes[0].completion_time,8)
        self.assertEqual(result.processes[1].completion_time,3)
        self.assertTrue(all(p.state==ProcessState.TERMINATED for p in result.processes))

    def test_mlfq_rejects_invalid_quantums(self):
        with self.assertRaises(ValueError):
            multilevel_feedback_queue([ServiceProcess(1,"A","X",2)],(2,0))

if __name__=="__main__":
    unittest.main()
