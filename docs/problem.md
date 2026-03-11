# Problem Statement

## Problem
While applying to jobs, creating many versions of a resume to match different job descriptions is time-consuming and confusing to manage manually.

## Why Existing Tools Fail
ATS scanners rely mostly on keyword matching and do not understand the semantic relationship between a candidate's experience and job requirements.

## Solution
Build a system that retrieves relevant experience from a user's resume and generates a job-specific resume grounded in the user's real work history.

## System Goal
Build a Resume Intelligence Engine that:
1. Ingests a user's resume (1-3 PDFs)
2. Converts resume sections into embeddings
3. Retrieves relevant experience for a job description
4. Generates a tailored resume grounded in the user's experience