
# Usage

## 1. Navigate to the Django Admin

Go to your Django admin interface. You will see a "Report Instances" section under the "Reports Ai" app.

## 2. Create a Report Instance

-   Click the "Add" button next to "Report Instances".
-   **Title**: Enter a descriptive title for your report.
-   **Report Type**: Choose a report type (e.g., `investor_update`).
-   **Git Repo Url**: Enter the HTTPS URL of the Git repository you want to analyze.
-   Click "Save".

## 3. Generate a Report

-   From the list of report instances, click on the one you just created.
-   In the top right corner, you will see a button that says "Generate/Regenerate Report". Click it.
-   The report generation will be queued as a background task. The status of the report will change to "Generating".

## 4. View the Report

-   Once the task is complete, the status will change to "Completed".
-   The generated summary will appear in the "Generated Report" field.
-   If the task fails, the status will be updated to "Failed". You can check the Celery logs for more details.
