import React, { useState } from 'react';
import ProductTypeList from '../components/ProductTypeList';
import ProductTypeForm from '../components/ProductTypeForm';
import useAdminStore from '../store/useAdminStore';
import { ProductType } from '../services/productTypeService';

// Import Part Category components
import PartCategoryManager from '../components/PartCategoryManager';

const AdminProductTypesPage: React.FC = () => {
  const [showProductTypeForm, setShowProductTypeForm] = useState(false);
  const [editingProductType, setEditingProductType] = useState<ProductType | null>(null);
  // Get selectedProductTypeId and potentially categories from the store
  const { productTypes, selectedProductTypeId } = useAdminStore(); 

  const handleAddNewProductType = () => {
    setEditingProductType(null);
    setShowProductTypeForm(true);
  };

  const handleEditProductType = (id: number) => {
    const ptToEdit = productTypes.find(pt => pt.id === id);
    if (ptToEdit) {
      setEditingProductType(ptToEdit);
      setShowProductTypeForm(true);
    }
  };

  const handleSaveProductType = () => {
    setShowProductTypeForm(false);
    setEditingProductType(null);
  };

  const handleCancelProductType = () => {
    setShowProductTypeForm(false);
    setEditingProductType(null);
  };

  return (
    <div style={{ position: 'relative', padding: '1rem', display: 'flex', gap: '2rem' }}>
      {/* Left Panel: Product Type Management */}
      <div style={{ flex: 1 }}>
        <h2>Product Type Management</h2>
        <button onClick={handleAddNewProductType} style={{ marginBottom: '1rem' }}>
          Add New Product Type
        </button>
        <ProductTypeList onEdit={handleEditProductType} onCreate={handleAddNewProductType} />
      </div>

      {/* Right Panel: Part Category Management */}
      <div style={{ flex: 1 }}>
        <h2>Part Categories</h2>
        {selectedProductTypeId ? (
          <PartCategoryManager productTypeId={selectedProductTypeId} />
        ) : (
          <p>Select a Product Type on the left to manage its categories.</p>
        )}
      </div>

      {/* Product Type Form Modal */}
      {showProductTypeForm && (
        <div style={modalOverlayStyle}>
          <ProductTypeForm
            initialData={editingProductType}
            onSave={handleSaveProductType}
            onCancel={handleCancelProductType}
          />
        </div>
      )}
    </div>
  );
};

// Basic modal styling (improve later)
const modalOverlayStyle: React.CSSProperties = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000, // Ensure it's above other content
};

export default AdminProductTypesPage; 