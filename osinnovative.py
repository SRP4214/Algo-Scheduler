import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

def fcfs(AT, BT):
    schedule = []
    start_timing = []
    end_timing = [] 
    n = len(AT)
    CPU = 0
    ATt = [0] * n
    NoP = n
    WT = [0] * n
    TAT = [0] * n
    start_time = [0] * n
    CT = [0] * n
    for i in range(n):
        ATt[i] = AT[i]
    while NoP > 0 :
        for i in range(n):
            if ATt[i] <= CPU:
                y = ATt[i]
                for j in range(n):
                    if (y > ATt[j]):
                        y = ATt[j]
                        i = j
                WT[i] = CPU - AT[i]
                start_time[i] = CPU
                start_timing.append(start_time[i])
                schedule.append(f"P{i+1}")
                end_timing.append(CPU + BT[i])
                CPU += BT[i]
                CT[i] = CPU
                TAT[i] = CPU - AT[i]
                # st.write(i, ATt[i])
                # st.write(ATt[i])
                ATt[i] = float('inf')
                NoP -= 1
                break
        else:
            schedule.append("Idle")
            start_timing.append(CPU)
            CPU += 1
            end_timing.append(CPU)
        # st.write(schedule)
    # st.write(start_timing, end_timing, schedule)
    return CT, TAT, WT, start_timing, end_timing, schedule

def sjf(AT, BT):
    schedule = []
    start_timing=[] 
    end_timing=[]
    CPU = 0
    n = len(AT)
    ST = [0] * n
    CT = [0] * n
    ATt = [0] * n
    NoP = n
    WT = [0] * n
    TAT = [0] * n
    processed = [False] * n

    for i in range(n):
        ATt[i] = AT[i]
    while NoP > 0:
        min_burst = float('inf')
        min_index = -1
        for i in range(n):
            if ATt[i] <= CPU and not processed[i] and BT[i] < min_burst:
                min_burst = BT[i]
                min_index = i

        if min_index == -1:
            start_timing.append(CPU)
            end_timing.append(CPU + 1)
            CPU += 1
            schedule.append(f"Idle")
            
        else:
            WT[min_index] = CPU - AT[min_index]
            ST[min_index] = CPU
            start_timing.append(CPU)
            CPU += BT[min_index]
            schedule.append(f"P{min_index + 1}")
            end_timing.append(start_timing[-1] + BT[min_index])
            CT[min_index] = CPU
            TAT[min_index] = CPU - AT[min_index]
            processed[min_index] = True
            NoP -= 1
    # st.write(start_timing, end_timing, schedule)
    return CT, TAT, WT, start_timing, end_timing, schedule

def round_robin(AT, BT, time_quantum):
    schedule = []
    n = len(AT)
    process_data = []
    for i in range(len(AT)):
        process_data.append([i, AT[i], BT[i], 0, BT[i]])
    start_time = []
    exit_time = []
    executed_process = []
    ready_queue = []
    s_time = 0
    process_data.sort(key=lambda x: x[1])
    
    while 1:
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                present = 0
                if len(ready_queue) != 0:
                    for k in range(len(ready_queue)):
                        if process_data[i][0] == ready_queue[k][0]:
                            present = 1
                
                if present == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                
                if len(ready_queue) != 0 and len(executed_process) != 0:
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                            ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            if ready_queue[0][2] > time_quantum:
                
                start_time.append(s_time)
                s_time = s_time + time_quantum
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_quantum
                ready_queue.pop(0)
            elif ready_queue[0][2] <= time_quantum:
                
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
                ready_queue.pop(0)
        elif len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            if normal_queue[0][2] > time_quantum:
                
                start_time.append(s_time)
                s_time = s_time + time_quantum
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_quantum
            elif normal_queue[0][2] <= time_quantum:
               
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
    for i in range(len(process_data)):
        turnaround_time = process_data[i][5] - process_data[i][1]
        process_data[i].append(turnaround_time)
    for i in range(len(process_data)):
        waiting_time = process_data[i][6] - process_data[i][4]
        process_data[i].append(waiting_time)
        
    process_data.sort(key=lambda x: x[0])
    CT = [0] * n
    WT = [0] * n
    TAT = [0] * n
    
    for i in range(n):
        CT[i] = process_data[i][5]
        TAT[i] = process_data[i][6]
        WT[i] = process_data[i][7]
   
    for i in range(len(executed_process)):
        schedule.append(f"P{executed_process[i] + 1}")
    
    return CT, TAT, WT, start_time, exit_time, schedule


def srtf(AT, BT):
    n = len(AT)
    process_data = []
    for i in range(len(AT)):
        process_data.append([i, AT[i], BT[i], 0, BT[i]])
    start_time = []
    exit_time = []
    s_time = 0
    executed_process = []
    process_data.sort(key=lambda x: x[1])
    while 1:
        ready_queue = []
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                ready_queue.append(temp)
                temp = []
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            ready_queue.sort(key=lambda x: x[2])
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            executed_process.append(ready_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == ready_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            if process_data[k][2] == 0:
                process_data[k][3] = 1
                process_data[k].append(e_time)
        if len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            executed_process.append(normal_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            if process_data[k][2] == 0:  
                process_data[k][3] = 1
                process_data[k].append(e_time)
    
    for i in range(len(process_data)):
        turnaround_time = process_data[i][5] - process_data[i][1]
        process_data[i].append(turnaround_time)
    
    for i in range(len(process_data)):
        waiting_time = process_data[i][6] - process_data[i][4]
        process_data[i].append(waiting_time)
    
    process_data.sort(key=lambda x: x[0])
    CT = [0] * n
    WT = [0] * n
    TAT = [0] * n
    
    for i in range(n):
        CT[i] = process_data[i][5]
        TAT[i] = process_data[i][6]
        WT[i] = process_data[i][7]
    schedule = []
    for i in range(len(executed_process)):
        schedule.append(f"P{executed_process[i] + 1}")
    return CT, TAT, WT, start_time, exit_time, schedule

def display_results(pn, at, bt, ct, wt, tat):
    df = pd.DataFrame({
        "Process": pn,
        "Arrival Time": at,
        "Burst Time": bt,
        "Completion Time": ct,
        "Turnaround Time": tat,
        "Waiting Time": wt
    })
    st.table(df)


def generate_gantt_chart(processes, algorithm, schedule, times):
    df = pd.DataFrame({
        "Task": [f"{process}" for process in schedule],
        "Start": [x[1] for x in times],
        "End": [x[0] for x in times],
    })

    df = df.sort_values(by='Task')
    
    color_map = {}
    color_counter = 0
    for process in set(schedule):
        if process not in color_map:
            color_map[process] = plt.cm.tab10(color_counter)
            color_counter += 1

    legend_patches = []
    for process in set(schedule):
        patch = plt.Rectangle((0, 0), 1, 1, color=color_map[process], label=process)
        legend_patches.append(patch)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df["Task"], df["End"] - df["Start"], left=df["Start"], color=[color_map[p] for p in df["Task"]])
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Processes")
    ax.set_title(f"{algorithm} Scheduling Gantt Chart")
    
    tick_vals = range(0, df["End"].max() + 1)  # Adjust for integer rounding

    # Set x-axis ticks and labels (consider using major and minor ticks for clarity)
    ax.set_xticks(tick_vals)
    major_tick_labels = [f"{t}" for t in tick_vals]  # Create labels for every ms
    ax.set_xticklabels(major_tick_labels, ha='right')
    
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.legend(handles=legend_patches)
    
    st.pyplot(fig)


def main():
    st.title("CPU Scheduler Engine")

    scheduler_options = ["First Come First Serve (FCFS)", "Shortest Job First (SJF)", "Round Robin", "Shortest Remaining Time First (SRTF)"]
    selected_option = st.selectbox("Select Scheduler Algorithm", scheduler_options)
    if selected_option == "Round Robin":
        quantum = st.number_input("Enter Time Quantum", min_value=1, step=1, value=1)
    
    n = st.number_input("Enter the number of processes", min_value=1, step=1, value=1)
    pn = []
    for i in range(n):
        x = f"P{i+1}"
        pn.append(x)
    at_input = []
    bt_input = []
    for i in range(n):
        at_input.append(st.number_input(f"Arrival Time for Process {i+1}", value=0, step=1))
        bt_input.append(st.number_input(f"Burst Time for Process {i+1}", value=1, step=1))
    ct = []
    tat = []
    wt = []
    stt = []
    et = []
    schd = []
    if st.button("Run"):
        if selected_option == "First Come First Serve (FCFS)":
            algorithm = "First Come First Serve (FCFS)"
            ct, tat, wt, stt, et, schd = fcfs(at_input, bt_input)
        elif selected_option == "Shortest Job First (SJF)":
            algorithm = "Shortest Job First (SJF)"
            ct, tat, wt, stt, et, schd = sjf(at_input, bt_input)
        elif selected_option == "Round Robin":
            algorithm = "Round Robin"
            ct, tat, wt, stt, et, schd = round_robin(at_input, bt_input, quantum)
        elif selected_option == "Shortest Remaining Time First (SRTF)":
            algorithm = "Shortest Remaining Time First (SRTF)"
            ct, tat, wt, stt, et, schd = srtf(at_input, bt_input)
        # st.write(stt, et)
        times = [(et[i], stt[i]) for i in range(len(stt))]
        display_results(pn, at_input, bt_input, ct, wt, tat)
        generate_gantt_chart(pn, algorithm, schd, times)
       
        

if __name__ == "__main__":
    main()