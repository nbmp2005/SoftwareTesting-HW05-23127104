# Execution and evidence

## Naming and directories

Use the real execution date:

- `23127104_Load_YYYYMMDD.jmx`
- `23127104_Stress_YYYYMMDD.jmx`
- `23127104_Spike_YYYYMMDD.jmx`

Match each raw JTL and report directory to its scenario. Do not rename a file to a date on which it was not run.

## Preflight

1. Record Git commit, OS, CPU, RAM, Java, JMeter, Node.js, and SUT version.
2. Start the backend and verify `http://localhost:3000` with a one-user smoke test.
3. Create or reset known data, then prove the admin credential works.
4. Close unrelated heavy applications and note unavoidable background load.
5. Synchronize visible clock/timezone and create a run ID.
6. Verify CSV row count is at least the number of concurrent users when rows are not recycled.
7. Run one iteration and inspect every response/assertion before load execution.

## Run

Use non-GUI mode for measurements. A typical command shape is:

```text
jmeter -n -t <plan.jmx> -l <raw.jtl> -e -o <empty-html-report-directory>
```

Do not overwrite an existing JTL or HTML directory. During each run, capture JMeter/terminal and Task Manager in the same frame. Record start/end time, workload parameters, CPU, memory, disk, and observations. Keep raw JTL unchanged.

## Account lockout recovery

Correct-password traffic should not increase the failed-login counter. If the admin is genuinely locked:

1. Stop the affected run; do not let repeated 403 responses pollute it.
2. Record the response and time as evidence.
3. Wait for the actual lock interval or reset the test database through the documented seed/reset procedure.
4. If resetting the database, record the command and acknowledge that all generated data was removed.
5. Re-run the one-user smoke test before restarting the scenario.

The current implementation uses 180 seconds despite the 30-second requirement, so verify the observed behavior and report it as a functional discrepancy rather than changing test expectations invisibly.

## Evidence inventory

For each scenario retain the JMX, input CSV, raw JTL, HTML report, workload screenshot, resource-monitor screenshot/same-frame capture, run notes, and relevant server log. Retain separate hardware evidence with hostname. Add video timestamps showing configuration, execution, resource behavior, results, human correction, and skill use.

Never manufacture missing evidence. Use `TODO (REAL EVIDENCE REQUIRED)` until captured.
