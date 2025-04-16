import React, { useState } from 'react';
import useAdminStore from '../store/useAdminStore';
import PartCategoryList from './PartCategoryList';
import PartCategoryForm from './PartCategoryForm';
import { PartCategory } from '../services/partCategoryService';

interface PartCategoryManagerProps {
  productTypeId: number;
}

const PartCategoryManager: React.FC<PartCategoryManagerProps> = ({ productTypeId }) => {
  const [showForm, setShowForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState<PartCategory | null>(null);
  const { partCategories, removePartCategory } = useAdminStore();

  const handleAddNew = () => {
    setEditingCategory(null);
    setShowForm(true);
  };

  const handleEdit = (id: number) => {
    const catToEdit = partCategories.find(pc => pc.id === id);
    if (catToEdit) {
      setEditingCategory(catToEdit);
      setShowForm(true);
    }
  };

  const handleDelete = (id: number, name: string) => {
    if (window.confirm(`Are you sure you want to delete category "${name}"? This will also delete associated options!`)) {
      removePartCategory(id);
    }
  };

  const handleSave = () => {
    setShowForm(false);
    setEditingCategory(null);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingCategory(null);
  };

  return (
    <div>
      <button onClick={handleAddNew} style={{ marginBottom: '1rem' }}>
        Add New Part Category
      </button>

      {/* Part Category List */} 
      <PartCategoryList onEdit={handleEdit} onDelete={handleDelete} />

      {/* Part Category Form Modal */} 
      {showForm && (
        <div style={modalOverlayStyle}> {/* Reuse or create shared modal style */} 
          <PartCategoryForm
            productTypeId={productTypeId}
            initialData={editingCategory}
            onSave={handleSave}
            onCancel={handleCancel}
          />
        </div>
      )}
    </div>
  );
};

// Basic modal styling (copied from AdminProductTypesPage - consider making reusable)
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
  zIndex: 1000,
};

export default PartCategoryManager; 