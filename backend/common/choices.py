from django.db import models

class AccountStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"


class TransactionReason(models.TextChoices):
    INITIAL_ALLOCATION = "INITIAL_ALLOCATION", "Initial Allocation"
    QUIZ_GENERATION = "QUIZ_GENERATION", "Quiz Generation"
    QUIZ_EVALUATION = "QUIZ_EVALUATION", "Quiz Evaluation"
    OCR_PROCESSING = "OCR_PROCESSING", "OCR Processing"
    FILE_PROCESSING = "FILE_PROCESSING", "File Processing"
    MANUAL_ADJUSTMENT = "MANUAL_ADJUSTMENT", "Manual Adjustment"
    REFUND = "REFUND", "Refund"

class TransactionType(models.TextChoices):
    CREDIT = "CREDIT", "Credit"
    DEBIT = "DEBIT", "Debit"

class WorkspaceStatus(models.TextChoices):
    EMPTY = "EMPTY", "Empty"
    READY_FOR_PROCESSING = "READY_FOR_PROCESSING", "Ready for Processing"
    PROCESSING = "PROCESSING", "Processing"
    READY = "READY", "Ready"
    FAILED = "FAILED", "Failed"
    ARCHIVED = "ARCHIVED", "Archived"

class WorkspaceStatus(models.TextChoices):
    EMPTY = "EMPTY", "Empty"
    READY_FOR_PROCESSING = "READY_FOR_PROCESSING", "Ready for Processing"
    PROCESSING = "PROCESSING", "Processing"
    READY = "READY", "Ready"
    FAILED = "FAILED", "Failed"
    ARCHIVED = "ARCHIVED", "Archived"