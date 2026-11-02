"""Sample citizen-service workload for scheduling demonstrations."""
from .models import ServiceProcess
def sample_requests():
    return [ServiceProcess(101,"Aarav","Birth certificate",5,0,2),ServiceProcess(102,"Diya","Address update",3,1,1),ServiceProcess(103,"Kabir","Pension enquiry",8,2,3),ServiceProcess(104,"Meera","Grievance filing",4,3,2)]
