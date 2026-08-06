from collections import defaultdict

total_trials = 0
total_frames = 0
total_duration = 0

trials_per_activity = defaultdict(int)
trials_per_camera = defaultdict(int)
trials_per_subject = defaultdict(int)
trials_per_task_parameters = defaultdict(int)

frames_per_activity = defaultdict(int)
frames_per_camera = defaultdict(int)
frames_per_subject = defaultdict(int)
frames_per_task_parameters = defaultdict(int)

duration_per_activity = defaultdict(float)
duration_per_camera = defaultdict(float)
duration_per_subject = defaultdict(int)
duration_per_task_parameters = defaultdict(int)

with open('../data/metadata.txt', 'r') as f:
    while True:
        # for file identifier lines (e.g., lift_c1-s1-sr2laf-GH010014)
        line = f.readline().rstrip()
        if not line:
            break
        activity, details = line.split('_')
        camera, subject, task_parameters, filename = details.split('-')
        if task_parameters in ['ll2rdf', 'lr2ldf']:
            activity = 'carry'
        task_parameters += f"_{activity}"

        # for trial lines (e.g., 24/704)
        while True:
            line = f.readline()
            if line == '\n': break
            if subject == 's1': # to exclude s1
                continue
            total_trials += 1
            trials_per_activity[activity] += 1
            trials_per_camera[camera] += 1
            trials_per_subject[subject] += 1
            trials_per_task_parameters[task_parameters] += 1

            start_frame, end_frame = map(int, line.split('/'))
            trial_frames = end_frame - start_frame + 1
            total_frames += trial_frames
            frames_per_activity[activity] += trial_frames
            frames_per_camera[camera] += trial_frames
            frames_per_subject[subject] += trial_frames
            frames_per_task_parameters[task_parameters] += trial_frames

            trial_duraiton = end_frame - start_frame
            total_duration += trial_duraiton
            duration_per_activity[activity] += trial_duraiton
            duration_per_camera[camera] += trial_duraiton
            duration_per_subject[subject] += trial_duraiton
            duration_per_task_parameters[task_parameters] += trial_duraiton
#########################################################
print(f"-----------------------------------------------")
print(f"Total Trials: {total_trials:,}")
print(f"Total Frames: {total_frames:,}")
print(f"Total Duration: {total_duration / 59.4 / 60:,.2f} minutes")
print(f"-----------------------------------------------")
for activity in ['push', 'pull', 'sit', 'stand', 'walk', 'lift', 'carry']:
    t_count = trials_per_activity[activity]
    f_count = frames_per_activity[activity]
    d_count = duration_per_activity[activity]
    print(f"{activity}: {t_count:,} trials ({t_count / total_trials * 100:.2f}%) | "
          f"{f_count:,} frames ({f_count / total_frames * 100:.2f}%) | "
          f"{d_count / 59.4 / 60:,.2f} minutes ({d_count / total_duration * 100:.2f}%)")
print(f"-----------------------------------------------")
for camera in ['c1', 'c2', 'c3', 'c4', 'c5']:
    t_count = trials_per_camera[camera]
    f_count = frames_per_camera[camera]
    d_count = duration_per_camera[camera]
    print(f"{camera}: {t_count:,} trials ({t_count / total_trials * 100:.2f}%) | "
          f"{f_count:,} frames ({f_count / total_frames * 100:.2f}%) | "
          f"{d_count / 59.4 / 60:,.2f} minutes ({d_count / total_duration * 100:.2f}%)")
print(f"-----------------------------------------------")
for subject in [f"s{i}" for i in range(1,26)]:
    t_count = trials_per_subject[subject]
    f_count = frames_per_subject[subject]
    d_count = duration_per_subject[subject]
    print(f"{subject}: {t_count:,} trials ({t_count / total_trials * 100:.2f}%) | "
          f"{f_count:,} frames ({f_count / total_frames * 100:.2f}%) | "
          f"{d_count / 59.4 / 60:,.2f} minutes ({d_count / total_duration * 100:.2f}%)")
print(f"-----------------------------------------------")
for task_parameters in trials_per_task_parameters.keys():
    t_count = trials_per_task_parameters[task_parameters]
    f_count = frames_per_task_parameters[task_parameters]
    d_count = duration_per_task_parameters[task_parameters]
    print(f"{task_parameters}: {t_count:,} trials ({t_count / total_trials * 100:.2f}%) | "
          f"{f_count:,} frames ({f_count / total_frames * 100:.2f}%) | "
          f"{d_count / 59.4 / 60:,.2f} minutes ({d_count / total_duration * 100:.2f}%)")
# print(f"-----------------------------------------------")
# print(total_trials
#       == sum(trials_per_activity.values())
#       == sum(trials_per_camera.values())
#       == sum(trials_per_subject.values())
#       == sum(trials_per_task_parameters.values()))
# print(total_frames
#       == sum(frames_per_activity.values())
#       == sum(frames_per_camera.values())
#       == sum(frames_per_subject.values())
#       == sum(frames_per_task_parameters.values()))
# print(total_duration
#       == sum(duration_per_activity.values())
#       == sum(duration_per_camera.values())
#       == sum(duration_per_subject.values())
#       == sum(duration_per_task_parameters.values()))