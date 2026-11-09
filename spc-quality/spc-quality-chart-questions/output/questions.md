# Chart questions and answer key

All data is synthetic. Answers are computed from the data, not typed by hand.

## spc-q01 (difficulty 1)
**Chart:** `fig1_control_chart.png`

**Question:** How many points on the control chart fall above the upper control limit (UCL)? Answer as a number of points.

**Answer:** 1  _(unit: points)_

**Solution:**

1. UCL = center line + 3 sigma = 2.042 + 3 x 0.252 = 2.798 percent (limits use days 1 to 20).
2. Points above 2.798: day 23 (3.1 percent).
3. Count = 1.

_Reading-error robustness: 100%_

## spc-q02 (difficulty 3)
**Chart:** `fig1_control_chart.png`

**Question:** On which day is the 8th consecutive point below the center line reached? Answer as a day number.

**Answer:** 31  _(unit: day)_

**Solution:**

1. Center line = 2.042 percent. Count consecutive points strictly below it, resetting at any point on or above it.
2. The last point above the line before the run is day 23; days 24 to 31 are all below.
3. The 8th consecutive point below the center line is day 31.

_Reading-error robustness: 100%_

## spc-q03 (difficulty 2)
**Chart:** `fig2_pareto_defect_causes.png`

**Question:** Starting with the largest cause, what is the smallest number of defect causes whose combined share of all defects reaches at least 80 percent? Answer as a number of causes.

**Answer:** 3  _(unit: causes)_

**Solution:**

1. Add the bars from the largest down and track the cumulative share (the cumulative line on the right axis).
2. Scratches: cumulative 48 of 106 = 45.3%
3. Misalignment: cumulative 79 of 106 = 74.5%
4. Missing component: cumulative 91 of 106 = 85.8%
5. Wrong label: cumulative 98 of 106 = 92.5%
6. Porosity: cumulative 103 of 106 = 97.2%
7. Other: cumulative 106 of 106 = 100.0%
8. The 80% mark is first reached with 3 causes.

_Reading-error robustness: 100%_

## spc-q04 (difficulty 2)
**Chart:** `fig2_pareto_defect_causes.png`

**Question:** What percent of all defects are caused by the top two causes combined? Give the answer in percent to the nearest whole percent.

**Answer:** 75  _(unit: percent)_

**Solution:**

1. Total defects = 106.
2. Top two causes = 48 + 31 = 79.
3. Share = 79 / 106 x 100 = 75 percent (nearest whole percent).

_Reading-error robustness: 100%_

## spc-q05 (difficulty 3)
**Chart:** `fig3_capability_histogram.png`

**Question:** Using the mean and the sample standard deviation printed on the histogram and the specification limits (LSL and USL), what is the process capability index Cpk? Give the answer to two decimal places.

**Answer:** 0.93  _(unit: index)_

**Solution:**

1. Read from the chart: mean = 50.014 mm, sample standard deviation s = 0.049 mm, LSL = 49.85 mm, USL = 50.15 mm.
2. Upper side: (USL - mean) / (3s) = (50.15 - 50.014) / (3 x 0.049) = 0.925.
3. Lower side: (mean - LSL) / (3s) = (50.014 - 49.85) / (3 x 0.049) = 1.116.
4. Cpk is the smaller value = 0.93.

_Reading-error robustness: 100%_

## Ambiguity check demos (flagged, not for submission)

- "How many points lie within 0.05 percentage points of the center line? Answer as a number of points." -> answer is sensitive to small reading errors (stable in 44% of trials)
- "Using the standard deviation shown, what is Cpk? Give the index to two decimal places." -> question uses a standard deviation without saying whether it is the sample or population value
