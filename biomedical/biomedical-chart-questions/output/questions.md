# Chart questions and answer key

All data is synthetic (not clinical data). Answers are computed from the data.

## bio-q01 (difficulty 1)
**Chart:** `fig1_dose_response_error_bars.png`

**Question:** What is the difference in mean systolic blood-pressure reduction between the 20 mg group and the placebo (0 mg) group? Give the answer in mmHg to one decimal place.

**Answer:** 11.6  _(unit: mmHg)_

**Solution:**

1. Read the mean reduction (the dot) for 20 mg: 15.0 mmHg, and for placebo (0 mg): 3.36 mmHg.
2. Difference = 15.0 - 3.36 = 11.6 mmHg.

_Reading-error robustness: 100%_

## bio-q02 (difficulty 3)
**Chart:** `fig1_dose_response_error_bars.png`

**Question:** The error bars show 95% confidence intervals. Which dose groups (in mg) have a 95% confidence interval that does not overlap the placebo group's interval?

**Answer:** [10, 20, 40]  _(unit: mg)_

**Solution:**

1. Placebo 95% CI = 1.63 to 5.09 mmHg (mean +/- the error bar).
2. A dose group does not overlap placebo if its lower limit is above the placebo upper limit.
3. 5 mg: 3.89 to 8.11 -> overlaps
4. 10 mg: 5.71 to 11.15 -> no overlap
5. 20 mg: 12.86 to 17.14 -> no overlap
6. 40 mg: 13.98 to 18.5 -> no overlap
7. Dose groups with no overlap: [10, 20, 40] mg.

_Reading-error robustness: 100%_

## bio-q03 (difficulty 2)
**Chart:** `fig2_heart_rate_over_time.png`

**Question:** Between hour 2 and hour 6, by what percentage does the treatment group's mean heart rate (bpm) fall? Give the answer in percent, to the nearest whole percent.

**Answer:** 11  _(unit: percent)_

**Solution:**

1. Treatment mean heart rate at hour 2: 70.1 bpm; at hour 6: 62.3 bpm.
2. Fall = 7.8 bpm. Percentage fall = 7.8 / 70.1 x 100 = 11.13 percent, which is 11 percent to the nearest whole percent.

_Reading-error robustness: 100%_

## bio-q04 (difficulty 3)
**Chart:** `fig2_heart_rate_over_time.png`

**Question:** At which hour (counting from the first dose at hour 0) does the placebo group's mean heart rate first exceed the treatment group's by at least 10 bpm?

**Answer:** 4  _(unit: hour)_

**Solution:**

1. Gap = placebo mean heart rate minus treatment mean heart rate, hour by hour.
2. At hour 3 the gap is 9.0 bpm (below 10).
3. At hour 4 the gap is 11.8 bpm (10 or more).
4. So the gap first reaches 10 bpm at hour 4.

_Reading-error robustness: 100%_

## bio-q05 (difficulty 3)
**Chart:** `fig3_dose_vs_reduction_scatter.png`

**Question:** Using the fitted line through all patients, how many mmHg of additional systolic blood-pressure reduction does the line predict for each extra 10 mg of dose? Give the answer in mmHg to one decimal place.

**Answer:** 3.3  _(unit: mmHg)_

**Solution:**

1. The fitted line over all 150 patients has slope 0.329 mmHg per mg (intercept 4.88 mmHg).
2. For each extra 10 mg: 0.329 x 10 = 3.3 mmHg additional reduction.

_Reading-error robustness: 100%_

## Ambiguity check demos (flagged, not for submission)

- "At which hour is the gap between the placebo and treatment heart rates largest? Answer as an hour." -> answer is sensitive to small reading errors (stable in 54% of trials)
- "Do the error bars of the 5 mg group and the placebo group overlap? Answer with the number of mg of the group." -> question mentions error bars without saying what they show (SD, SEM or 95% CI)
