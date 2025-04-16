import React from 'react';
import useAdminStore from '../store/useAdminStore';

interface PartCategoryListProps {
  onEdit: (id: number) => void;
  onDelete: (id: number, name: string) => void;
}

const PartCategoryList: React.FC<PartCategoryListProps> = ({ onEdit, onDelete }) => {
  const {
    partCategories,
    partCategoryLoading: loading,
    partCategoryError: error,
    selectedProductTypeId,
  } = useAdminStore();

  if (loading) return <p>Loading categories...</p>;
  if (error) return <p style={{ color: 'red' }}>Error loading categories: {error}</p>;
  if (!selectedProductTypeId) return <p>No product type selected.</p>;
  if (partCategories.length === 0) return <p>No categories found for this product type.</p>;

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
      <thead>
        <tr>
          <th style={thStyle}>ID</th>
          <th style={thStyle}>Name</th>
          <th style={thStyle}>Order</th>
          <th style={thStyle}>Actions</th>
        </tr>
      </thead>
      <tbody>
        {partCategories.map((pc) => (
          <tr key={pc.id}>
            <td style={tdStyle}>{pc.id}</td>
            <td style={tdStyle}>{pc.name}</td>
            <td style={tdStyle}>{pc.display_order}</td>
            <td style={tdStyle}>
              <button onClick={() => onEdit(pc.id)} style={{ marginRight: '0.5rem' }}>Edit</button>
              <button onClick={() => onDelete(pc.id, pc.name)}>Delete</button>
              {/* Add button/link to manage options later */}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

// Basic styling (reuse or move to CSS)
const thStyle: React.CSSProperties = {
  border: '1px solid #ddd',
  padding: '8px',
  textAlign: 'left',
  backgroundColor: '#f2f2f2'
};

const tdStyle: React.CSSProperties = {
  border: '1px solid #ddd',
  padding: '8px'
};

export default PartCategoryList; 