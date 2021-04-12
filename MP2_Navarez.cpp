/*
 A. Navarez's Submission for CMSC 125's MP 2
 Note: Printing of processes depends on the order in which they are finished.

 References:
 https://stackoverflow.com/questions/15601973/stl-priority-queue-of-c-with-struct
*/
#include <iostream>
#include <queue>
#include <functional>
#include <deque>
#include <fstream>
#include <sstream>
#include <typeinfo>

using namespace std;

// implementing a min priority queue based on different components
struct job{
	int process;
	int arrival;
	int burst;
	int priority;
	int remaining;
	int turnaround;
};

void print(job j){
	cout << j.process << " arrival:" << j.arrival << " burst:" << j.burst << " prio:" << j.priority << " rem:" << j.remaining << endl;
}

void print_prio(priority_queue<job, deque<job>, function<bool(job,job)>> f){
	while(!f.empty()){
		print(f.top());
		f.pop();
	}
}

bool fcfs_compare(job a, job b){
	return (a.arrival > b.arrival) || (a.arrival == b.arrival && a.process > b.process);
}

bool sjf_compare(job a, job b){
	return (a.burst > b.burst) || (a.burst == b.burst && a.arrival > b.arrival);
}

bool priority_compare(job a, job b){
	return (a.priority > b.priority) || (a.priority == b.priority && a.arrival > b.arrival) || (a.priority == b.priority && a.arrival ==  b.arrival && a.process > b.process);
}

bool srpt_compare(job a, job b){
	return (a.remaining > b.remaining) || (a.remaining == b.remaining && a.arrival > b.arrival);
}

priority_queue<job, deque<job>, function<bool(job,job)>> create_priority_queue(string type){
	if(type =="fcfs"){
		priority_queue<job, deque<job>, function<bool(job,job)>> f(fcfs_compare);
		return f;
	}
	else if(type == "sjf"){	
		priority_queue<job, deque<job>, function<bool(job,job)>> f(sjf_compare);
		return f;
	}
	else if(type == "srpt"){
		priority_queue<job, deque<job>, function<bool(job,job)>> f(srpt_compare);
		return f;
	}
	else{
		priority_queue<job, deque<job>, function<bool(job,job)>> f(priority_compare);
		return f;
	}
}

void print_values(int ctt, int cwt, int size){
	cout << "Average waiting time: " << (cwt*1.0)/size << " ms" << endl;
	cout << "Average turnaround time: " << (ctt*1.0)/size << " ms" << endl;
}

void nonpreemptive_scheduling(priority_queue<job, deque<job>, function<bool(job,job)>> f, deque<job> jobs){
	int wt, tt, cwt, ctt;
	wt = tt = cwt = ctt = 0;
	for(job j: jobs)
		f.push(j);
	while(!f.empty()){
		job j = f.top();
		wt = tt;
		tt = tt + j.burst; 
		cout << j.process << " = wt:" << wt << ", tt:" << tt << endl;
		f.pop();
		cwt += wt;
		ctt += tt;
	}
  print_values(ctt, cwt, jobs.size());
}

void srpt_scheduling(deque<job> jobs){
	int cwt = 0, timer=0, ctt = 0, jobsize  = jobs.size();
	deque<job> ord;
	priority_queue<job, deque<job>, function<bool(job,job)>> newf = create_priority_queue("srpt");

	job j = jobs.front();

	while(true){
		if(!newf.empty())
			j = newf.top();
		if(j.remaining - 1 > 0){
			// not finished
			j.remaining -= 1; 
			ord.push_back(j);
			timer++;
		}
		else{
			// finished
			timer++;
			j.turnaround = timer;
			j.remaining = 0;
			cwt += j.turnaround - j.burst - j.arrival;
			ctt += timer;	
			cout << j.process << " = wt:" << j.turnaround - j.burst - j.arrival << ", tt:" << j.turnaround << endl;
		}
		if(!newf.empty())
			newf.pop();
		// get nth job if still 'arriving'
		if(timer < jobsize)
			ord.push_back(jobs.at(timer));
		// getting valid jobs to prep heapify
		while(!newf.empty()){
			ord.push_back(newf.top());
			newf.pop();
		}
		// heapify
		while(!ord.empty()){
			newf.push(ord.front());
			ord.pop_front();
		}
		if(ord.empty() && newf.empty())
			break;
	}
  print_values(ctt, cwt, jobs.size());
}

void time_based_scheduling(deque<job> jobs, int timect){
	int cwt = 0, timer=0, ctt = 0, jobsize = jobs.size();

	job j;
	while(!jobs.empty()){
		for(int i=0; i<jobs.size(); i++){
			j = jobs.at(i);
			if(j.remaining - timect > 0){
				j.remaining = j.remaining - timect;
				jobs.at(i) = j;
				timer += timect;
			}
			else{
				timer += j.remaining; // do not wait for time to finish
				j.turnaround = timer;
				j.remaining = 0;
				cwt += j.turnaround - j.burst;	
				ctt += timer;
				jobs.erase(jobs.begin()+i);
				--i;
				cout << j.process << " = wt:" << j.turnaround - j.burst << ", tt:" << j.turnaround << endl;
			}
		}
	}
  print_values(ctt, cwt, jobsize);
}

deque<job> process(string filename){
	ifstream file;
	file.open(filename);
	string line;

	deque<job> v;
	bool first = false;
	while(getline(file, line)){
		if(!first){
			first = true;
			continue;
		}
		stringstream ss(line);
		int i = 0;
		int vals[4];
		while(getline(ss, line, (char) 9)){
			if(line.length() > 0){
				vals[i] = stoi(line);
				i++;
			}
		}
		job newj = {vals[0], vals[1], vals[2], vals[3], vals[2], 0};
		v.push_back(newj);
	}
	
	file.close();
	return v;
}

int main(){
	int choice = 0;
  string filename;

  while(choice < 1 || choice > 3){
    cout << "Input the number of choice:\n1. Process 1\n2. Process 2\n3. Process 3\n";
    cin >> choice;
    switch(choice){
      case 1:
        filename = "process1.txt";
        break;
      case 2:
        filename = "process2.txt";
        break;
      case 3:
        filename = "process3.txt";
        break;
      default:
        break;
    }
  }
  deque<job> jobs = process(filename);
  
  cout << "FCFS:\n";
	nonpreemptive_scheduling(create_priority_queue("fcfs"), jobs);
	cout << endl;
	cout << "SJF:\n";
	nonpreemptive_scheduling(create_priority_queue("sjf"), jobs);
	cout << endl;
	cout << "PRIORITY:\n";
	nonpreemptive_scheduling(create_priority_queue("priority"), jobs);
	cout << endl;
	cout << "SRPT:\n";
	srpt_scheduling(jobs);
	cout << endl;
	cout << "ROUND-ROBIN:\n";
	time_based_scheduling(jobs, 3);
	cout << endl;
	return 0;
}
