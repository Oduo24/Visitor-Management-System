import {
  useMemo,
  useState,
  type FormEvent,
} from "react";
 
import axios from "axios";
 
import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
 
import {
  createUser,
  deleteUser,
  getUsers,
  updateUser,
} from "../../api/users.api";
 
import {
  getOrganizations,
} from "../../api/organizations.api";
 
import {
  getDepartments,
} from "../../api/departments.api";
 
import {
  getRoles,
} from "../../api/roles.api";
 
import {
  getSites,
} from "../../api/sites.api";
 
import {
  createUserSiteRole,
  deleteUserSiteRole,
  getUserSiteRoles,
} from "../../api/userSiteRoles.api";
 
import type {
  User,
  CreateUserPayload,
  UpdateUserPayload,
} from "../../types/user";
 
 
interface UserFormState {
  organization_id: string;
  department_id: string | null;
 
  first_name: string;
  last_name: string;
 
  email: string;
  phone: string;
 
  employee_number: string;
  job_title: string;
 
  profile_photo_url: string;
 
  password: string;
 
  is_active: boolean;
}
 
 
const EMPTY_FORM: UserFormState = {
  organization_id: "",
  department_id: null,
 
  first_name: "",
  last_name: "",
 
  email: "",
  phone: "",
 
  employee_number: "",
  job_title: "",
 
  profile_photo_url: "",
 
  password: "",
 
  is_active: true,
};
 
 
function getErrorMessage(
  error: unknown,
  fallback: string
) {
 
  if (
    axios.isAxiosError(error)
  ) {
 
    const data =
      error.response?.data as {
        message?: string;
        error?: string;
      } | undefined;
 
    return (
      data?.message
      ??
      data?.error
      ??
      fallback
    );
  }
 
  return fallback;
}
 
 
export function UserListPage() {
 
  const queryClient =
    useQueryClient();
 
 
  const [
    search,
    setSearch,
  ] = useState("");
 
 
  const [
    editingUser,
    setEditingUser,
  ] = useState<User | null>(
    null
  );
 
 
  const [
    showForm,
    setShowForm,
  ] = useState(false);
 
 
  const [
    form,
    setForm,
  ] = useState<UserFormState>({
    ...EMPTY_FORM,
  });
 
 
  const [
    formError,
    setFormError,
  ] = useState<string | null>(
    null
  );
 
 
  const [
    accessUser,
    setAccessUser,
  ] = useState<User | null>(
    null
  );
 
 
  const [
    selectedSiteId,
    setSelectedSiteId,
  ] = useState("");
 
 
  const [
    selectedRoleId,
    setSelectedRoleId,
  ] = useState("");
 
 
  const [
    accessError,
    setAccessError,
  ] = useState<string | null>(
    null
  );
 
 
  const usersQuery =
    useQuery({
      queryKey: ["users"],
      queryFn: getUsers,
    });
 
 
  const organizationsQuery =
    useQuery({
      queryKey: ["organizations"],
      queryFn: getOrganizations,
    });
 
 
  const departmentsQuery =
    useQuery({
      queryKey: ["departments"],
      queryFn: getDepartments,
    });
 
 
  const sitesQuery =
    useQuery({
      queryKey: ["sites"],
      queryFn: getSites,
    });
 
 
  const rolesQuery =
    useQuery({
      queryKey: ["roles"],
      queryFn: getRoles,
    });
 
 
  const assignmentsQuery =
    useQuery({
      queryKey: [
        "user-site-roles",
      ],
      queryFn:
        getUserSiteRoles,
    });
 
 
  const users =
    usersQuery.data ?? [];
 
  const organizations =
    organizationsQuery.data ?? [];
 
  const departments =
    departmentsQuery.data ?? [];
 
  const sites =
    sitesQuery.data ?? [];
 
  const roles =
    rolesQuery.data ?? [];
 
  const assignments =
    assignmentsQuery.data ?? [];
 
 
  const organizationMap =
    useMemo<
      Map<string, string>
    >(
      () => {
 
        const map =
          new Map<
            string,
            string
          >();
 
        organizations.forEach(
          (organization) => {
 
            map.set(
              organization.id,
              organization.name
            );
          }
        );
 
        return map;
      },
      [organizations]
    );
 
 
  const departmentMap =
    useMemo<
      Map<string, string>
    >(
      () => {
 
        const map =
          new Map<
            string,
            string
          >();
 
        departments.forEach(
          (department) => {
 
            map.set(
              department.id,
              department.name
            );
          }
        );
 
        return map;
      },
      [departments]
    );
 
 
  const siteMap =
    useMemo<
      Map<string, string>
    >(
      () => {
 
        const map =
          new Map<
            string,
            string
          >();
 
        sites.forEach(
          (site) => {
 
            map.set(
              site.id,
              site.name
            );
          }
        );
 
        return map;
      },
      [sites]
    );
 
 
  const roleMap =
    useMemo<
      Map<string, string>
    >(
      () => {
 
        const map =
          new Map<
            string,
            string
          >();
 
        roles.forEach(
          (role) => {
 
            map.set(
              role.id,
              role.name
            );
          }
        );
 
        return map;
      },
      [roles]
    );
 
 
  const saveMutation =
    useMutation({
 
      mutationFn: async () => {
 
        if (editingUser) {
 
          const payload:
            UpdateUserPayload = {
 
            organization_id:
              form.organization_id,
 
            department_id:
              form.department_id,
 
            first_name:
              form.first_name.trim(),
 
            last_name:
              form.last_name.trim(),
 
            email:
              form.email.trim(),
 
            phone:
              form.phone.trim()
              || null,
 
            employee_number:
              form.employee_number
                .trim()
              || null,
 
            job_title:
              form.job_title.trim()
              || null,
 
            profile_photo_url:
              form.profile_photo_url
                .trim()
              || null,
 
            is_active:
              form.is_active,
          };
 
 
          if (
            form.password.trim()
          ) {
 
            payload.password =
              form.password;
          }
 
 
          return updateUser(
            editingUser.id,
            payload
          );
        }
 
 
        const payload:
          CreateUserPayload = {
 
          organization_id:
            form.organization_id,
 
          department_id:
            form.department_id,
 
          first_name:
            form.first_name.trim(),
 
          last_name:
            form.last_name.trim(),
 
          email:
            form.email.trim(),
 
          phone:
            form.phone.trim()
            || null,
 
          employee_number:
            form.employee_number
              .trim()
            || null,
 
          job_title:
            form.job_title.trim()
            || null,
 
          profile_photo_url:
            form.profile_photo_url
              .trim()
            || null,
 
          password:
            form.password,
 
          is_active:
            form.is_active,
        };
 
 
        return createUser(
          payload
        );
      },
 
 
      onSuccess: async () => {
 
        closeForm();
 
        await queryClient
          .invalidateQueries({
            queryKey: ["users"],
          });
      },
 
 
      onError: (error) => {
 
        setFormError(
          getErrorMessage(
            error,
            "Unable to save user."
          )
        );
      },
 
    });
 
 
  const statusMutation =
    useMutation({
 
      mutationFn: ({
        user,
        active,
      }: {
        user: User;
        active: boolean;
      }) => {
 
        return updateUser(
          user.id,
          {
            is_active:
              active,
          }
        );
      },
 
 
      onSuccess: async () => {
 
        await queryClient
          .invalidateQueries({
            queryKey: ["users"],
          });
      },
 
    });
 
 
  const deleteMutation =
    useMutation({
 
      mutationFn:
        deleteUser,
 
 
      onSuccess: async () => {
 
        await queryClient
          .invalidateQueries({
            queryKey: ["users"],
          });
      },
 
 
      onError: (error) => {
 
        window.alert(
          getErrorMessage(
            error,
            "Unable to delete user."
          )
        );
      },
 
    });
 
 
  const addAccessMutation =
    useMutation({
 
      mutationFn: () => {
 
        if (!accessUser) {
          throw new Error(
            "No user selected."
          );
        }
 
        return createUserSiteRole({
          user_id:
            accessUser.id,
 
          site_id:
            selectedSiteId,
 
          role_id:
            selectedRoleId,
        });
      },
 
 
      onSuccess: async () => {
 
        setSelectedSiteId("");
        setSelectedRoleId("");
        setAccessError(null);
 
        await queryClient
          .invalidateQueries({
            queryKey: [
              "user-site-roles",
            ],
          });
      },
 
 
      onError: (error) => {
 
        setAccessError(
          getErrorMessage(
            error,
            "Unable to assign access."
          )
        );
      },
 
    });
 
 
  const removeAccessMutation =
    useMutation({
 
      mutationFn:
        deleteUserSiteRole,
 
 
      onSuccess: async () => {
 
        await queryClient
          .invalidateQueries({
            queryKey: [
              "user-site-roles",
            ],
          });
      },
 
 
      onError: (error) => {
 
        setAccessError(
          getErrorMessage(
            error,
            "Unable to remove access."
          )
        );
      },
 
    });
 
 
  const filteredUsers =
    useMemo(() => {
 
      const term =
        search
          .trim()
          .toLowerCase();
 
      if (!term) {
        return users;
      }
 
      return users.filter(
        (user) => {
 
          const searchable = [
            user.full_name,
            user.first_name,
            user.last_name,
            user.email,
            user.phone,
            user.employee_number,
            user.job_title,
 
            organizationMap.get(
              user.organization_id
            ),
 
            user.department_id
              ? departmentMap.get(
                  user.department_id
                )
              : null,
          ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();
 
          return searchable.includes(
            term
          );
        }
      );
 
    }, [
      users,
      search,
      organizationMap,
      departmentMap,
    ]);
 
 
  const availableDepartments =
    departments.filter(
      (department) =>
        department.organization_id
        === form.organization_id
        &&
        department.is_active
    );
 
 
  const accessSites =
    accessUser
      ? sites.filter(
          (site) =>
            site.organization_id
            ===
            accessUser.organization_id
            &&
            site.is_active
        )
      : [];
 
 
  const accessRoles =
    accessUser
      ? roles.filter(
          (role) =>
            role.organization_id
            ===
            accessUser.organization_id
            &&
            role.is_active
        )
      : [];
 
 
  const userAssignments =
    accessUser
      ? assignments.filter(
          (assignment) =>
            assignment.user_id
            === accessUser.id
        )
      : [];
 
 
  function openCreateForm() {
 
    setEditingUser(null);
 
    setForm({
      ...EMPTY_FORM,
 
      organization_id:
        organizations.length === 1
          ? organizations[0].id
          : "",
    });
 
    setFormError(null);
 
    setShowForm(true);
  }
 
 
  function openEditForm(
    user: User
  ) {
 
    setEditingUser(user);
 
    setForm({
      organization_id:
        user.organization_id,
 
      department_id:
        user.department_id,
 
      first_name:
        user.first_name,
 
      last_name:
        user.last_name,
 
      email:
        user.email,
 
      phone:
        user.phone ?? "",
 
      employee_number:
        user.employee_number ?? "",
 
      job_title:
        user.job_title ?? "",
 
      profile_photo_url:
        user.profile_photo_url ?? "",
 
      password: "",
 
      is_active:
        user.is_active,
    });
 
    setFormError(null);
 
    setShowForm(true);
  }
 
 
  function closeForm() {
 
    setShowForm(false);
    setEditingUser(null);
 
    setForm({
      ...EMPTY_FORM,
    });
 
    setFormError(null);
  }
 
 
  function handleSubmit(
    event: FormEvent
  ) {
 
    event.preventDefault();
 
    setFormError(null);
 
 
    if (!form.organization_id) {
 
      setFormError(
        "Organization is required."
      );
 
      return;
    }
 
 
    if (
      form.first_name
        .trim()
        .length < 2
    ) {
 
      setFormError(
        "First name must contain at least 2 characters."
      );
 
      return;
    }
 
 
    if (
      form.last_name
        .trim()
        .length < 2
    ) {
 
      setFormError(
        "Last name must contain at least 2 characters."
      );
 
      return;
    }
 
 
    if (!form.email.trim()) {
 
      setFormError(
        "Email is required."
      );
 
      return;
    }
 
 
    if (
      !editingUser
      &&
      form.password.length < 8
    ) {
 
      setFormError(
        "Password must contain at least 8 characters."
      );
 
      return;
    }
 
 
    if (
      editingUser
      &&
      form.password
      &&
      form.password.length < 8
    ) {
 
      setFormError(
        "New password must contain at least 8 characters."
      );
 
      return;
    }
 
 
    saveMutation.mutate();
  }
 
 
  const loading =
    usersQuery.isLoading
    ||
    organizationsQuery.isLoading
    ||
    departmentsQuery.isLoading
    ||
    sitesQuery.isLoading
    ||
    rolesQuery.isLoading
    ||
    assignmentsQuery.isLoading;
 
 
  if (loading) {
 
    return (
      <div>
        Loading user administration...
      </div>
    );
  }
 
 
  return (
    <div className="page">
 
      <div className="page-heading">
 
        <div>
 
          <h1>
            Users
          </h1>
 
          <p>
            Manage employees, hosts,
            application access and site
            roles.
          </p>
 
        </div>
 
 
        <button
          type="button"
          className="button"
          onClick={
            openCreateForm
          }
        >
          Add User
        </button>
 
      </div>
 
 
      <div className="list-toolbar">
 
        <input
          type="search"
          placeholder="Search users..."
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value
            )
          }
        />
 
      </div>
 
 
      {showForm && (
 
        <section className="detail-card">
 
          <h2>
            {
              editingUser
                ? "Edit User"
                : "Add User"
            }
          </h2>
 
 
          <form
            onSubmit={
              handleSubmit
            }
          >
 
            <div className="form-grid">
 
              <div className="form-field">
 
                <label>
                  Organization *
                </label>
 
                <select
                  value={
                    form.organization_id
                  }
                  onChange={(event) => {
 
                    setForm(
                      (current) => ({
                        ...current,
 
                        organization_id:
                          event.target.value,
 
                        department_id:
                          null,
                      })
                    );
                  }}
                >
 
                  <option value="">
                    Select organization
                  </option>
 
                  {organizations.map(
                    (organization) => (
 
                      <option
                        key={
                          organization.id
                        }
                        value={
                          organization.id
                        }
                      >
                        {
                          organization.name
                        }
                      </option>
 
                    )
                  )}
 
                </select>
 
              </div>
 
 
              <div className="form-field">
 
                <label>
                  Department
                </label>
 
                <select
                  value={
                    form.department_id
                    ?? ""
                  }
                  onChange={(event) =>
                    setForm(
                      (current) => ({
                        ...current,
 
                        department_id:
                          event.target.value
                          || null,
                      })
                    )
                  }
                >
 
                  <option value="">
                    No department
                  </option>
 
                  {availableDepartments.map(
                    (department) => (
 
                      <option
                        key={
                          department.id
                        }
                        value={
                          department.id
                        }
                      >
                        {
                          department.name
                        }
                      </option>
 
                    )
                  )}
 
                </select>
 
              </div>
 
 
              <UserInput
                label="First Name *"
                value={
                  form.first_name
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      first_name: value,
                    })
                  )
                }
              />
 
 
              <UserInput
                label="Last Name *"
                value={
                  form.last_name
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      last_name: value,
                    })
                  )
                }
              />
 
 
              <UserInput
                label="Email *"
                type="email"
                value={
                  form.email
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      email: value,
                    })
                  )
                }
              />
 
 
              <UserInput
                label="Phone"
                value={
                  form.phone
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      phone: value,
                    })
                  )
                }
              />
 
 
              <UserInput
                label="Employee Number"
                value={
                  form.employee_number
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      employee_number:
                        value,
                    })
                  )
                }
              />
 
 
              <UserInput
                label="Job Title"
                value={
                  form.job_title
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      job_title: value,
                    })
                  )
                }
              />
 
 
              <UserInput
                label={
                  editingUser
                    ? "New Password"
                    : "Password *"
                }
                type="password"
                value={
                  form.password
                }
                onChange={(value) =>
                  setForm(
                    (current) => ({
                      ...current,
                      password: value,
                    })
                  )
                }
              />
 
            </div>
 
 
            <label className="checkbox-field">
 
              <input
                type="checkbox"
                checked={
                  form.is_active
                }
                onChange={(event) =>
                  setForm(
                    (current) => ({
                      ...current,
 
                      is_active:
                        event.target
                          .checked,
                    })
                  )
                }
              />
 
              Active user
 
            </label>
 
 
            {formError && (
              <div className="form-error">
                {formError}
              </div>
            )}
 
 
            <div className="table-actions">
 
              <button
                type="submit"
                className="button"
                disabled={
                  saveMutation.isPending
                }
              >
                {
                  saveMutation.isPending
                    ? "Saving..."
                    : "Save User"
                }
              </button>
 
 
              <button
                type="button"
                onClick={
                  closeForm
                }
              >
                Cancel
              </button>
 
            </div>
 
          </form>
 
        </section>
 
      )}
 
 
      <div className="table-wrapper">
 
        <table>
 
          <thead>
            <tr>
              <th>User</th>
              <th>Organization</th>
              <th>Department</th>
              <th>Job Title</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
 
 
          <tbody>
 
            {filteredUsers.map(
              (user) => (
 
                <tr key={user.id}>
 
                  <td>
 
                    <strong>
                      {user.full_name}
                    </strong>
 
                    <div className="table-secondary">
                      {user.email}
                    </div>
 
                  </td>
 
 
                  <td>
                    {
                      organizationMap.get(
                        user.organization_id
                      )
                      ?? "-"
                    }
                  </td>
 
 
                  <td>
                    {
                      user.department_id
                        ? (
                            departmentMap.get(
                              user.department_id
                            )
                            ?? "-"
                          )
                        : "-"
                    }
                  </td>
 
 
                  <td>
                    {
                      user.job_title
                      ?? "-"
                    }
                  </td>
 
 
                  <td>
                    {
                      user.is_active
                        ? "ACTIVE"
                        : "INACTIVE"
                    }
                  </td>
 
 
                  <td>
 
                    <div className="table-actions">
 
                      <button
                        type="button"
                        onClick={() =>
                          openEditForm(
                            user
                          )
                        }
                      >
                        Edit
                      </button>
 
 
                      <button
                        type="button"
                        onClick={() => {
 
                          setAccessUser(
                            user
                          );
 
                          setAccessError(
                            null
                          );
                        }}
                      >
                        Manage Access
                      </button>
 
 
                      <button
                        type="button"
                        onClick={() =>
                          statusMutation.mutate({
                            user,
                            active:
                              !user.is_active,
                          })
                        }
                      >
                        {
                          user.is_active
                            ? "Deactivate"
                            : "Activate"
                        }
                      </button>
 
 
                      {!user.is_active && (
 
                        <button
                          type="button"
                          onClick={() => {
 
                            if (
                              window.confirm(
                                `Permanently delete ${user.full_name}?`
                              )
                            ) {
 
                              deleteMutation
                                .mutate(
                                  user.id
                                );
                            }
                          }}
                        >
                          Delete
                        </button>
 
                      )}
 
                    </div>
 
                  </td>
 
                </tr>
 
              )
            )}
 
          </tbody>
 
        </table>
 
      </div>
 
 
      {accessUser && (
 
        <section className="detail-card access-panel">
 
          <div className="section-heading">
 
            <div>
 
              <h2>
                Access — {
                  accessUser.full_name
                }
              </h2>
 
              <p className="form-help">
                Assign this user a role
                at a specific site.
              </p>
 
            </div>
 
 
            <button
              type="button"
              onClick={() => {
 
                setAccessUser(null);
 
                setSelectedSiteId("");
                setSelectedRoleId("");
 
                setAccessError(null);
              }}
            >
              Close
            </button>
 
          </div>
 
 
          <div className="form-grid">
 
            <div className="form-field">
 
              <label>
                Site
              </label>
 
              <select
                value={
                  selectedSiteId
                }
                onChange={(event) =>
                  setSelectedSiteId(
                    event.target.value
                  )
                }
              >
 
                <option value="">
                  Select site
                </option>
 
                {accessSites.map(
                  (site) => (
 
                    <option
                      key={site.id}
                      value={site.id}
                    >
                      {site.name}
                    </option>
 
                  )
                )}
 
              </select>
 
            </div>
 
 
            <div className="form-field">
 
              <label>
                Role
              </label>
 
              <select
                value={
                  selectedRoleId
                }
                onChange={(event) =>
                  setSelectedRoleId(
                    event.target.value
                  )
                }
              >
 
                <option value="">
                  Select role
                </option>
 
                {accessRoles.map(
                  (role) => (
 
                    <option
                      key={role.id}
                      value={role.id}
                    >
                      {role.name}
                    </option>
 
                  )
                )}
 
              </select>
 
            </div>
 
          </div>
 
 
          <button
            type="button"
            className="button"
            disabled={
              !selectedSiteId
              ||
              !selectedRoleId
              ||
              addAccessMutation
                .isPending
            }
            onClick={() =>
              addAccessMutation.mutate()
            }
          >
            {
              addAccessMutation.isPending
                ? "Assigning..."
                : "Assign Access"
            }
          </button>
 
 
          {accessError && (
            <div className="form-error">
              {accessError}
            </div>
          )}
 
 
          <h3>
            Current Access
          </h3>
 
 
          {userAssignments.length === 0 ? (
 
            <p>
              No site roles assigned.
            </p>
 
          ) : (
 
            <div className="table-wrapper">
 
              <table>
 
                <thead>
                  <tr>
                    <th>Site</th>
                    <th>Role</th>
                    <th></th>
                  </tr>
                </thead>
 
 
                <tbody>
 
                  {userAssignments.map(
                    (assignment) => (
 
                      <tr
                        key={
                          assignment.id
                        }
                      >
 
                        <td>
                          {
                            siteMap.get(
                              assignment.site_id
                            )
                            ?? "-"
                          }
                        </td>
 
 
                        <td>
                          {
                            roleMap.get(
                              assignment.role_id
                            )
                            ?? "-"
                          }
                        </td>
 
 
                        <td>
 
                          <button
                            type="button"
                            disabled={
                              removeAccessMutation
                                .isPending
                            }
                            onClick={() =>
                              removeAccessMutation
                                .mutate(
                                  assignment.id
                                )
                            }
                          >
                            Remove
                          </button>
 
                        </td>
 
                      </tr>
 
                    )
                  )}
 
                </tbody>
 
              </table>
 
            </div>
 
          )}
 
        </section>
 
      )}
 
    </div>
  );
}
 
 
function UserInput({
  label,
  value,
  type = "text",
  onChange,
}: {
  label: string;
  value: string;
  type?: string;
  onChange: (
    value: string
  ) => void;
}) {
 
  return (
    <div className="form-field">
 
      <label>
        {label}
      </label>
 
      <input
        type={type}
        value={value}
        onChange={(event) =>
          onChange(
            event.target.value
          )
        }
      />
 
    </div>
  );
}