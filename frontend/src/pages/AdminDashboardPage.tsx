import React from 'react';
import AdminProductTypesPage from './AdminProductTypesPage'; // Import the new page

const AdminDashboardPage: React.FC = () => {
  // Dashboard implementation (CRUD interfaces) will go here in EPIC-03
  return (
    <div>
      {/* We can add layout/navigation here later */}
      <AdminProductTypesPage />
    </div>
  );
};

export default AdminDashboardPage; 