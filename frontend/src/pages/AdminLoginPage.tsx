import React from 'react';
import AdminLoginForm from '../components/AdminLoginForm'; // Import the form

const AdminLoginPage: React.FC = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <AdminLoginForm />
    </div>
  );
};

export default AdminLoginPage; 