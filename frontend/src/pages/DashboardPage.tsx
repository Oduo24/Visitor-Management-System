import {
  useState,
} from "react";
 
import {
  useQuery,
} from "@tanstack/react-query";
 
import {
  getVisitDashboard,
} from "../api/dashboard.api";
 
import {
  getSites,
} from "../api/sites.api";
 
import type {
  DashboardFilters,
} from "../types/dashboard";
 
 
export function DashboardPage() {
 
  const [
    filters,
    setFilters,
  ] = useState<DashboardFilters>({
    site_id: "",
    visit_type: "",
    start_date: "",
    end_date: "",
  });
 
 
  const dashboardQuery =
    useQuery({
 
      queryKey: [
        "visit-dashboard",
        filters,
      ],
 
      queryFn: () =>
        getVisitDashboard(
          filters
        ),
 
    });
 
 
  const sitesQuery =
    useQuery({
 
      queryKey: [
        "sites",
      ],
 
      queryFn:
        getSites,
 
    });
 
 
  const dashboard =
    dashboardQuery.data;
 
  const sites =
    sitesQuery.data ?? [];
 
 
  function updateFilter<
    K extends keyof DashboardFilters
  >(
    key: K,
    value: DashboardFilters[K]
  ) {
 
    setFilters(
      (current) => ({
        ...current,
        [key]: value,
      })
    );
  }
 
 
  function clearFilters() {
 
    setFilters({
      site_id: "",
      visit_type: "",
      start_date: "",
      end_date: "",
    });
  }
 
 
  if (
    dashboardQuery.isLoading
  ) {
 
    return (
      <div>
        Loading dashboard...
      </div>
    );
  }
 
 
  if (
    dashboardQuery.isError
  ) {
 
    return (
      <div className="form-error">
        Unable to load dashboard.
      </div>
    );
  }
 
 
  if (!dashboard) {
    return null;
  }
 
 
  return (
    <div className="page">
 
      <div className="page-heading">
 
        <div>
 
          <h1>
            Dashboard
          </h1>
 
          <p>
            Overview of visitor
            activity and visit status.
          </p>
 
        </div>
 
      </div>
 
 
      {/* Filters */}
 
      <section className="detail-card">
 
        <div className="section-heading">
 
          <h2>
            Filters
          </h2>
 
 
          <button
            type="button"
            onClick={
              clearFilters
            }
          >
            Clear Filters
          </button>
 
        </div>
 
 
        <div className="form-grid">
 
          <div className="form-field">
 
            <label>
              Site
            </label>
 
            <select
              value={
                filters.site_id
                ?? ""
              }
              onChange={(event) =>
                updateFilter(
                  "site_id",
                  event.target.value
                )
              }
            >
 
              <option value="">
                All Sites
              </option>
 
 
              {sites.map(
                (site) => (
 
                  <option
                    key={
                      site.id
                    }
                    value={
                      site.id
                    }
                  >
                    {site.name}
                  </option>
 
                )
              )}
 
            </select>
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              Visit Type
            </label>
 
            <select
              value={
                filters.visit_type
                ?? ""
              }
              onChange={(event) =>
                updateFilter(
                  "visit_type",
                  event.target.value
                )
              }
            >
 
              <option value="">
                All Types
              </option>
 
              <option value="PREBOOK">
                Prebook
              </option>
 
              <option value="WALK_IN">
                Walk-in
              </option>
 
            </select>
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              From
            </label>
 
            <input
              type="date"
              value={
                filters.start_date
                ?? ""
              }
              onChange={(event) =>
                updateFilter(
                  "start_date",
                  event.target.value
                )
              }
            />
 
          </div>
 
 
          <div className="form-field">
 
            <label>
              To
            </label>
 
            <input
              type="date"
              value={
                filters.end_date
                ?? ""
              }
              onChange={(event) =>
                updateFilter(
                  "end_date",
                  event.target.value
                )
              }
            />
 
          </div>
 
        </div>
 
      </section>
 
 
      {/* Summary Cards */}
 
      <div className="dashboard-grid">
 
        <DashboardCard
          title="Total Visits"
          value={
            dashboard.total_visits
          }
        />
 
        <DashboardCard
          title="Pending Approval"
          value={
            dashboard.pending_approval
          }
        />
 
        <DashboardCard
          title="Approved"
          value={
            dashboard.approved
          }
        />
 
        <DashboardCard
          title="Checked In"
          value={
            dashboard.checked_in
          }
        />
 
        <DashboardCard
          title="Checked Out"
          value={
            dashboard.checked_out
          }
        />
 
      </div>
 
 
      <div className="dashboard-section-grid">
 
        {/* Status Breakdown */}
 
        <section className="detail-card">
 
          <h2>
            Status Breakdown
          </h2>
 
 
          {
            Object.entries(
              dashboard
                .status_breakdown
            ).length === 0
              ? (
                  <p>
                    No visit data.
                  </p>
                )
              : (
                  <div className="breakdown-list">
 
                    {Object.entries(
                      dashboard
                        .status_breakdown
                    ).map(
                      ([
                        status,
                        count,
                      ]) => (
 
                        <BreakdownRow
                          key={
                            status
                          }
                          label={
                            formatLabel(
                              status
                            )
                          }
                          count={
                            count
                          }
                          total={
                            dashboard
                              .total_visits
                          }
                        />
 
                      )
                    )}
 
                  </div>
                )
          }
 
        </section>
 
 
        {/* Visit Type Breakdown */}
 
        <section className="detail-card">
 
          <h2>
            Visit Types
          </h2>
 
 
          {
            Object.entries(
              dashboard
                .visit_type_breakdown
            ).length === 0
              ? (
                  <p>
                    No visit data.
                  </p>
                )
              : (
                  <div className="breakdown-list">
 
                    {Object.entries(
                      dashboard
                        .visit_type_breakdown
                    ).map(
                      ([
                        type,
                        count,
                      ]) => (
 
                        <BreakdownRow
                          key={
                            type
                          }
                          label={
                            formatLabel(
                              type
                            )
                          }
                          count={
                            count
                          }
                          total={
                            dashboard
                              .total_visits
                          }
                        />
 
                      )
                    )}
 
                  </div>
                )
          }
 
        </section>
 
      </div>
 
    </div>
  );
}
 
 
function DashboardCard({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
 
  return (
    <div className="dashboard-card">
 
      <div className="dashboard-card-title">
        {title}
      </div>
 
      <div className="dashboard-card-value">
        {value}
      </div>
 
    </div>
  );
}
 
 
function BreakdownRow({
  label,
  count,
  total,
}: {
  label: string;
  count: number;
  total: number;
}) {
 
  const percentage =
    total > 0
      ? Math.round(
          (
            count
            /
            total
          )
          * 100
        )
      : 0;
 
 
  return (
    <div className="breakdown-row">
 
      <div className="breakdown-heading">
 
        <span>
          {label}
        </span>
 
        <strong>
          {count}
        </strong>
 
      </div>
 
 
      <div className="breakdown-track">
 
        <div
          className="breakdown-fill"
          style={{
            width:
              `${percentage}%`,
          }}
        />
 
      </div>
 
 
      <div className="table-secondary">
        {percentage}% of visits
      </div>
 
    </div>
  );
}
 
 
function formatLabel(
  value: string
) {
 
  return value
    .replaceAll(
      "_",
      " "
    )
    .toLowerCase()
    .replace(
      /\b\w/g,
      (letter) =>
        letter.toUpperCase()
    );
}