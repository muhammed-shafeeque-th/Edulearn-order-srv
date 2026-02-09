

from enum import Enum


class EVENT_TOPICS(Enum):
    # ====== AUTH DOMAIN EVENTS ======
    AUTH_USER_CREATED = 'auth.user.created.v1'
    AUTH_USER_REGISTERED = 'auth.user.registered.v1'
    AUTH_USER_LOGIN = 'auth.user.login.v1'
    AUTH_OTP_REQUESTED = 'auth.otp.requested.v1'
    AUTH_OTP_VERIFIED = 'auth.otp.verified.v1'
    AUTH_OTP_VERIFICATION_FAILED = 'auth.otp.verification.failed.v1'
    AUTH_MFA_ENABLED = 'auth.mfa.enabled.v1'
    AUTH_MFA_DISABLED = 'auth.mfa.disabled.v1'
    AUTH_ACCOUNT_LOCKED = 'auth.account.locked.v1'
    AUTH_ACCOUNT_UNLOCKED = 'auth.account.unlocked.v1'
    AUTH_TOKEN_ISSUED = 'auth.token.issued.v1'
    AUTH_TOKEN_REFRESHED = 'auth.token.refreshed.v1'
    AUTH_TOKEN_REVOKED = 'auth.token.revoked.v1'

    # ====== USER DOMAIN EVENTS ======
    USER_CREATED = 'user.created.v1'
    USER_UPDATED = 'user.updated.v1'
    USER_DELETED = 'user.deleted.v1'
    USER_PROFILE_COMPLETED = 'user.profile.completed.v1'
    USER_PROFILE_UPDATED = 'user.profile.updated.v1'
    USER_STATUS_CHANGED = 'user.status.changed.v1'
    USER_ROLE_ASSIGNED = 'user.role.assigned.v1'
    USER_ROLE_REVOKED = 'user.role.revoked.v1'
    USER_INSTRUCTOR_REGISTERED = 'user.instructor.registered.v1'
    USER_INSTRUCTOR_VERIFIED = 'user.instructor.verified.v1'
    USER_INSTRUCTOR_REJECTED = 'user.instructor.rejected.v1'

    # ====== NOTIFICATION DOMAIN EVENTS ======
    NOTIFICATION_SENT_EMAIL = 'notification.sent.email.v1'
    NOTIFICATION_SENT_SMS = 'notification.sent.sms.v1'
    NOTIFICATION_SENT_IN_APP = 'notification.sent.in-app.v1'
    NOTIFICATION_SENT_PUSH = 'notification.sent.push.v1'
    NOTIFICATION_DELIVERED = 'notification.delivered.v1'
    NOTIFICATION_FAILED = 'notification.failed.v1'
    NOTIFICATION_VIEWED = 'notification.viewed.v1'
    NOTIFICATION_DISMISSED = 'notification.dismissed.v1'

    NOTIFICATION_REQUEST_EMAIL = 'notification.request.email.v1'
    NOTIFICATION_REQUEST_SMS = 'notification.request.sms.v1'
    NOTIFICATION_REQUEST_IN_APP = 'notification.request.in-app.v1'
    NOTIFICATION_REQUEST_PUSH = 'notification.request.push.v1'
    NOTIFICATION_REQUEST_GENERAL = 'notification.request.general.v1'
    NOTIFICATION_EVENT_GENERAL = 'notification.event.general.v1'

    # Auth-specific notification requests
    NOTIFICATION_REQUEST_AUTH_OTP = 'notification.request.auth.otp.v1'
    NOTIFICATION_REQUEST_AUTH_FORGOT_PASSWORD = 'notification.request.auth.forgot-password.v1'
    NOTIFICATION_REQUEST_AUTH_ACCOUNT_CREATED = 'notification.request.auth.account-created.v1'

    # Notification event channels (for multi-channel workflows)
    NOTIFICATION_EMAIL_CHANNEL = 'notification.channel.email.v1'
    NOTIFICATION_SMS_CHANNEL = 'notification.channel.sms.v1'
    NOTIFICATION_PUSH_CHANNEL = 'notification.channel.push.v1'
    NOTIFICATION_IN_APP_CHANNEL = 'notification.channel.in-app.v1'

    # ====== COURSE DOMAIN EVENTS ======
    COURSE_CREATED = 'course.created.v1'
    COURSE_UPDATED = 'course.updated.v1'
    COURSE_DELETED = 'course.deleted.v1'
    COURSE_PUBLISHED = 'course.published.v1'
    COURSE_UNPUBLISHED = 'course.unpublished.v1'
    COURSE_ARCHIVED = 'course.archived.v1'
    COURSE_RESTORED = 'course.restored.v1'
    COURSE_ENROLLMENT_CREATED = 'course.enrollment.created.v1'
    COURSE_ENROLLMENT_CANCELLED = 'course.enrollment.cancelled.v1'
    COURSE_ENROLLMENT_COMPLETED = 'course.enrollment.completed.v1'
    COURSE_ENROLLMENT_FAILED = 'course.enrollment.failed.v1'
    COURSE_PROGRESS_STARTED = 'course.progress.started.v1'
    COURSE_PROGRESS_UPDATED = 'course.progress.updated.v1'
    COURSE_PROGRESS_COMPLETED = 'course.progress.completed.v1'
    COURSE_REVIEW_SUBMITTED = 'course.review.submitted.v1'

    # Order - course workflow
    ORDER_COURSE_CREATED = 'order.course.created.v1'
    ORDER_COURSE_UPDATED = 'order.course.updated.v1'
    ORDER_COURSE_CANCELLED = 'order.course.cancelled.v1'
    ORDER_COURSE_EXPIRED = 'order.course.expired.v1'
    ORDER_COURSE_SUCCEEDED = 'order.course.succeeded.v1'
    ORDER_COURSE_FAILED = 'order.course.failed.v1'
    ORDER_COURSE_REFUNDED = 'order.course.refunded.v1'
    ORDER_COURSE_FULFILLED = 'order.course.fulfilled.v1'

    # ====== PAYMENT DOMAIN EVENTS ======
    PAYMENT_ORDER_INITIATED = 'payment.order.initiated.v1'
    PAYMENT_ORDER_SUCCEEDED = 'payment.order.succeeded.v1'
    PAYMENT_ORDER_FAILED = 'payment.order.failed.v1'
    PAYMENT_ORDER_PENDING = 'payment.order.pending.v1'
    PAYMENT_ORDER_CANCELLED = 'payment.order.cancelled.v1'
    PAYMENT_ORDER_TIMEOUT = 'payment.order.timeout.v1'
    PAYMENT_ORDER_REFUNDED = 'payment.order.refunded.v1'
    PAYMENT_ORDER_DISPUTED = 'payment.order.disputed.v1'
    PAYMENT_ORDER_PROCESSING = 'payment.order.processing.v1'
    PAYMENT_ORDER_COMPLETED = 'payment.order.completed.v1'
    PAYMENT_CHARGEBACK_INITIATED = 'payment.chargeback.initiated.v1'
    PAYMENT_CHARGEBACK_RESOLVED = 'payment.chargeback.resolved.v1'
    PAYMENT_PAYOUT_INITIATED = 'payment.payout.initiated.v1'
    PAYMENT_PAYOUT_COMPLETED = 'payment.payout.completed.v1'

    # ====== SESSION & AUTHENTICATION EVENTS ======
    SESSION_CREATED = 'session.created.v1'
    SESSION_REFRESHED = 'session.refreshed.v1'
    SESSION_TERMINATED = 'session.terminated.v1'
    SESSION_EXPIRED = 'session.expired.v1'
    SESSION_CANCELLED = 'session.cancelled.v1'
    SESSION_EXTENDED = 'session.extended.v1'
    SESSION_INVALIDATED = 'session.invalidated.v1'

    # ====== DLQ (DEAD LETTER QUEUES) ======
    DLQ_USER_SERVICE = 'dlq.user.service.v1'
    DLQ_COURSE_SERVICE = 'dlq.course.service.v1'
    DLQ_ORDER_SERVICE = 'dlq.order.service.v1'
    DLQ_PAYMENT_SERVICE = 'dlq.payment.service.v1'
    DLQ_NOTIFICATION_SERVICE = 'dlq.notification.service.v1'
    DLQ_API_GATEWAY = 'dlq.api.gateway.v1'
    DLQ_SESSION_SERVICE = 'dlq.session.service.v1'
    DLQ_AUTH_SERVICE = 'dlq.auth.service.v1'

    # ====== MISC/GENERAL ======
    AUDIT_LOG_EVENT = 'audit.log.event.v1'
    HEALTH_CHECK = 'internal.healthcheck.v1'

    # # Auth-related events
    # AUTH_USER_CREATE = 'auth.user.create'
    # AUTH_USER_REGISTER = 'auth.user.register'
    # AUTH_USER_LOGIN = 'auth.user.login'
    # AUTH_USER_LOGOUT = 'auth.user.logout'

    # # User-related events
    # USER_USER_UPDATED = "user.user.updated"
    # USER_USER_CREATED = "user.user.created"
    # USER_USER_DELETED = "user.user.deleted"

    # USER_INSTRUCTOR_REGISTERED = "user.instructor.registered"

    # # Order-related events
    # ORDER_COURSE_CREATED = "order.course.created"
    # ORDER_COURSE_UPDATED = "order.course.updated"
    # ORDER_COURSE_CANCELLED = "order.course.cancelled"
    # ORDER_COURSE_EXPIRED = "order.course.expired"
    # ORDER_COURSE_SUCCEEDED = "order.course.succeeded"
    # ORDER_COURSE_FAILED = "order.course.failed"
    # ORDER_COURSE_REFUNDED = "order.course.refunded"
    # ORDER_COURSE_FULFILLED = "order.course.fulfilled"

    # # Payment-related events
    # PAYMENT_ORDER_INITIATED = "payment.order.initiated"
    # PAYMENT_ORDER_SUCCEEDED = "payment.order.succeeded"
    # PAYMENT_ORDER_FAILED = "payment.order.failed"
    # PAYMENT_ORDER_PENDING = "payment.order.pending"
    # PAYMENT_ORDER_CANCELLED = "payment.order.cancelled"
    # PAYMENT_ORDER_TIMEOUT = "payment.order.timeout"
    # PAYMENT_ORDER_REFUNDED = "payment.order.refunded"
    # PAYMENT_ORDER_DISPUTED = "payment.order.disputed"

    # # Notification events
    # NOTIFICATION_EMAIL_SENT = "notification.email.sent"
    # NOTIFICATION_SMS_SENT = "notification.sms.sent"
    # NOTIFICATION_INAPP_SENT = "notification.inapp.sent"

    # # Session/Authentication events
    # SESSION_SESSION_CREATED = "session.session.created"
    # SESSION_SESSION_CANCELLED = "session.session.cancelled"
    # SESSION__SESSION_EXPIRED = "session.session.expired"
    # SESSION_SESSION_TERMINATED = "session.session.terminated"

    # # Inventory/Course events (if relevant for orders)
    # COURSE_COURSE_CREATED = "course.course.created"
    # COURSE_COURSE_UPDATED = "course.course.updated"
    # COURSE_PROGRESS_STARTED = "course.progress.started"
    # COURSE_PROGRESS_COMPLETED = "course.progress.completed"
    # COURSE_ENROLLMENT_CREATED = "course.enrollment.created"
    # COURSE_ENROLLMENT_CANCELLED = "course.enrollment.cancelled"
