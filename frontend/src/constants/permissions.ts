export const Permission = {
  VISITOR_CREATE: "visitor_create",
  VISITOR_READ: "visitor_read",
  VISITOR_UPDATE: "visitor_update",
  VISITOR_DELETE: "visitor_delete",

  VISIT_CREATE: "visit_create",
  VISIT_READ: "visit_read",
  VISIT_UPDATE: "visit_update",
  VISIT_DELETE: "visit_delete",

  VISIT_APPROVE: "visit_approve",
  VISIT_CHECKIN: "visit_checkin",
  VISIT_CHECKOUT: "visit_checkout",

  HOST_CREATE: "host_create",
  HOST_READ: "host_read",
  HOST_UPDATE: "host_update",
  HOST_DELETE: "host_delete",

  USER_CREATE: "user_create",
  USER_READ: "user_read",
  USER_UPDATE: "user_update",
  USER_DELETE: "user_delete",

  REPORT_VIEW: "report_view",

  SETTINGS_MANAGE: "settings_manage",
} as const;