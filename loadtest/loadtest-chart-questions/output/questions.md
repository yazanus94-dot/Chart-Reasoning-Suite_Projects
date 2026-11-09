# Chart questions and answer key

All data is synthetic. Answers are computed from the data, not typed by hand.

## lt-q01 (difficulty 2)
**Chart:** `fig1_throughput_vs_response_time.png`

**Question:** On the throughput line, at which number of virtual users does throughput first stop growing by more than 2 percent compared with the previous 10-user step?

**Answer:** 130  _(unit: users)_

**Solution:**

1. Compare each throughput point with the previous one (10-user steps); growth = (new - old) / old.
2. Growth up to 120 users is above 2% at every step.
3. From 120 to 130 users: (481.7 - 481.9) / 481.9 = -0.0%, which is 2% or less.
4. So throughput first stops growing by more than 2% at 130 users.

_Reading-error robustness: 100%_

## lt-q02 (difficulty 2)
**Chart:** `fig1_throughput_vs_response_time.png`

**Question:** By what percentage does the average response time (right axis, in ms) increase between 100 users and 160 users? Give the answer in percent to one decimal place.

**Answer:** 75.5  _(unit: percent)_

**Solution:**

1. Read average response time at 100 users: 159.8 ms; at 160 users: 280.5 ms.
2. Change = 280.5 - 159.8 = 120.7 ms.
3. Percentage increase = 120.7 / 159.8 x 100 = 75.5 percent.

_Reading-error robustness: 100%_

## lt-q03 (difficulty 1)
**Chart:** `fig3_error_rate_vs_users.png`

**Question:** What is the highest user level, in steps of 10, at which the error rate is still at or below the 1 percent SLA line?

**Answer:** 120  _(unit: users)_

**Solution:**

1. The SLA line is at 1.0 percent error rate.
2. Error rate at 120 users is 0.89 percent, which is at or below the line.
3. Error rate at 130 users is 1.32 percent, which is above the line.
4. So the highest level that still meets the SLA is 120 users.

_Reading-error robustness: 100%_

## lt-q04 (difficulty 2)
**Chart:** `fig2_response_time_percentiles.png`

**Question:** At 120 users, how many times larger is the p99 response time than the p50 response time? Give the ratio to two decimal places.

**Answer:** 3.75  _(unit: ratio)_

**Solution:**

1. In the grouped bars at 120 users, p99 = 509.7 ms and p50 = 135.9 ms.
2. Ratio = 509.7 / 135.9 = 3.75.

_Reading-error robustness: 100%_

## lt-q05 (difficulty 3)
**Chart:** `fig1_throughput_vs_response_time.png + fig3_error_rate_vs_users.png`

**Question:** Using the error-rate chart, find the first user level at which the error rate is above the 1 percent SLA line. How many times larger is the average response time at that level than at 10 users? Give the ratio to two decimal places.

**Answer:** 1.63  _(unit: ratio)_

**Solution:**

1. Find the first user level where the error rate is above the SLA line: 130 users (third chart).
2. Read average response time at 130 users: 187.9 ms (first chart).
3. Read average response time at 10 users: 115.1 ms.
4. Ratio = 187.9 / 115.1 = 1.63 times.

_Reading-error robustness: 100%_

## Ambiguity check demo

The question "At how many users is throughput at its highest point? Answer in users." was **flagged** and should not be submitted: answer is sensitive to small reading errors (stable in 53% of trials)
