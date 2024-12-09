// Lấy danh sách nhân viên
async function loadEmployees() {
  const response = await fetch("http://localhost:3000/employees");
  const employees = await response.json();
  const tableBody = document.querySelector("#employees-table tbody");
  tableBody.innerHTML = "";

  employees.forEach((employee) => {
    const row = `
      <tr>
        <td>${employee.full_name}</td>
        <td>${employee.role}</td>
        <td>${employee.email}</td>
        <td>******</td>
        <td>
          <button onclick="editEmployee(${employee.employee_id})">Sửa</button>
          <button onclick="deleteEmployee(${employee.employee_id})">Xóa</button>
        </td>
      </tr>
    `;
    tableBody.innerHTML += row;
  });
}

// Gọi hàm khi trang load
document.addEventListener("DOMContentLoaded", () => {
  loadEmployees();
});
