resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "trips-load-datapipeline"
  role_arn = aws_iam_role.trips_step_function_role.arn

  definition = <<EOF
{
  "Comment": "Trips datapipeline",
  "StartAt": "raw_job",
  "States": {
    "raw_job": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "raw_job",
        "Arguments": {
          "--datetime.$": "$.datetime"
        }
      },
      "Next": "Parallel",
      "ResultPath": null
    },
    "Parallel": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "dimregions_job",
          "States": {
            "dimregions_job": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "dimregions_job",
                "Arguments": {
                  "--datetime.$": "$.datetime"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "dimdatasources_job",
          "States": {
            "dimdatasources_job": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "dimdatasources_job",
                "Arguments": {
                  "--datetime.$": "$.datetime"
                }
              },
              "End": true
            }
          }
        }
      ],
      "Next": "facttrips_job",
      "ResultPath": null
    },
    "facttrips_job": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "facttrips_job",
        "Arguments": {
          "--datetime.$": "$.datetime"
        }
      },
      "End": true
    }
  }
}
EOF
}