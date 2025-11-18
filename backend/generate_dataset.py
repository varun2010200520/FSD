import pandas as pd
import numpy as np

np.random.seed(42)
n = 6000

# Generate synthetic data with realistic correlations
attendance = np.random.uniform(25, 100, n)
study_hours = np.random.uniform(0.5, 5.5, n)
internal_marks = np.random.uniform(25, 100, n)
assignments = np.random.randint(0, 11, n)
activities = np.random.randint(0, 6, n)

# Outcome based on weighted score
outcome = []
for a, s, m, asg, act in zip(attendance, study_hours, internal_marks, assignments, activities):
    score = (a * 0.25 + m * 0.40 + s * 10 + asg * 3 + act * 2) / 1.7
    outcome.append('Pass' if score >= 55 else 'Fail')

df = pd.DataFrame({
    'attendance': np.round(attendance, 1),
    'study_hours': np.round(study_hours, 1),
    'internal_marks': np.round(internal_marks, 1),
    'assignments_submitted': assignments,
    'activities_participated': activities,
    'outcome': outcome
})

df.to_csv(r'..\dataset\students.csv', index=False)
print(f"Generated {len(df)} rows")
print(df['outcome'].value_counts())
print("\nDataset preview:")
print(df.head())
