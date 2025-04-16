import React, { useEffect } from 'react';
import useAdminStore from '../store/useAdminStore'; // Update import

interface ProductTypeListProps {
  onEdit: (id: number) => void; // Callback to handle edit button click
  onCreate: () => void; // Callback to handle create button click
}

const ProductTypeList: React.FC<ProductTypeListProps> = ({ onEdit, onCreate }) => {
  const {
    productTypes,
    productTypeLoading: loading, // Use renamed state variable
    productTypeError: error,     // Use renamed state variable
    fetchProductTypes,
    removeProductType,
    selectProductType, // Get the action to select a product type
  } = useAdminStore();

  useEffect(() => {
    fetchProductTypes();
  }, [fetchProductTypes]);

  const handleDelete = (id: number, name: string) => {
    // Basic confirmation
    if (window.confirm(`Are you sure you want to delete product type "${name}"? This will also delete associated categories and options!`)) {
      removeProductType(id);
    }
  };

  // Handle clicking on a product type row to select it
  const handleRowClick = (id: number) => {
    selectProductType(id);
  };

  if (loading) return <p>Loading product types...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      {/* Move Add button to parent page */}
      {/* <button onClick={onCreate} style={{ marginBottom: '1rem' }}> */}
      {/*  Add New Product Type */}
      {/* </button> */}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={thStyle}>ID</th>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Description</th>
            <th style={thStyle}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {productTypes.map((pt) => (
            <tr key={pt.id} onClick={() => handleRowClick(pt.id)} style={{ cursor: 'pointer' }}>
              <td style={tdStyle}>{pt.id}</td>
              <td style={tdStyle}>{pt.name}</td>
              <td style={tdStyle}>{pt.description}</td>
              <td style={tdStyle}>
                <button onClick={(e) => { e.stopPropagation(); onEdit(pt.id); }} style={{ marginRight: '0.5rem' }}>Edit</button>
                <button onClick={(e) => { e.stopPropagation(); handleDelete(pt.id, pt.name); }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Basic styling (can be moved to CSS)
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

export default ProductTypeList; 