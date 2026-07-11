import React, { useState } from 'react';
import Navbar from '../common/Navbar';
import './Workspace.css';

// ── SVG icon helpers ─────────────────────────────────────────────────────────
const Icon = {
  edit: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
  ),
  plus: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  ),
  play: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="5 3 19 12 5 21 5 3" />
    </svg>
  ),
  stats: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  ),
  trash: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    </svg>
  ),
  file: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  )
};

export default function Workspace({ workspaceName: initialWorkspaceName = 'My Workspace', lastEdited = 'Just now' }) {
  const [activePage, setActivePage] = useState('workspace');
  const [searchValue, setSearchValue] = useState('');
  
  // Local state for workspace metadata
  const [workspaceName, setWorkspaceName] = useState(initialWorkspaceName);
  const [isDeleted, setIsDeleted] = useState(false);
  
  // Modal states
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [editNameValue, setEditNameValue] = useState(workspaceName);

  // Dummy arrays to render the empty squares
  const quizzesTaken = [1, 2, 3];
  const filesInWorkspace = [1, 2, 3];

  if (isDeleted) {
    return (
      <div className="ws-root db-root" id="workspace-page-root">
        <Navbar activePage={activePage} onNavigate={setActivePage} notificationCount={0} searchValue={searchValue} onSearchChange={setSearchValue} />
        <main className="ws-deleted-main">
           <div className="db-card ws-deleted-card">
             <div className="ws-deleted-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
             </div>
             <h2 className="ws-deleted-title">Workspace Deleted</h2>
             <p className="ws-deleted-text">This workspace has been successfully removed. You can now navigate back to your dashboard.</p>
           </div>
        </main>
      </div>
    );
  }

  return (
    <div className="ws-root db-root" id="workspace-page-root">
      {/* ── Universal Navbar ── */}
      <Navbar
        activePage={activePage}
        onNavigate={setActivePage}
        notificationCount={0}
        searchValue={searchValue}
        onSearchChange={setSearchValue}
      />

      <main className="db-main ws-main" id="workspace-main-content">
        {/* ══ Centre column ══ */}
        <div className="db-col-main ws-col-main">
          
          {/* Workspace Header */}
          <div className="ws-header db-card" id="workspace-header-section">
            <span>
            <span className="ws-title" id="workspace-title">{workspaceName}</span>
            <span className="ws-meta" id="workspace-last-edited">(Last edited at: {lastEdited}) </span>
            </span>
          </div>

          <div className="ws-sections db-card" id="workspace-content-cards">
            {/* Quizzes Section */}
            <section className="ws-section" id="workspace-quizzes-section">
              <h2 className="ws-section-title">Quizzes</h2>
              <div className="ws-cards-grid" id="workspace-quizzes-grid">
                {quizzesTaken.map((item, idx) => (
                  <div key={`quiz-${idx}`} id={`workspace-quiz-card-${idx}`} className="ws-empty-square">
                    <span className="ws-empty-icon">{Icon.file}</span>
                  </div>
                ))}
              </div>
            </section>

            {/* Files Section */}
            <section className="ws-section" id="workspace-files-section">
              <h2 className="ws-section-title">Material</h2>
              <div className="ws-cards-grid" id="workspace-files-grid">
                {filesInWorkspace.map((item, idx) => (
                  <div key={`file-${idx}`} id={`workspace-file-card-${idx}`} className="ws-empty-square">
                    <span className="ws-empty-icon">{Icon.file}</span>
                  </div>
                ))}
              </div>
            </section>
          </div>

        </div>

        {/* ══ Sidebar ══ */}
        <aside className="db-sidebar ws-sidebar" id="workspace-sidebar">
          
          {/* Actions Card */}
          <section className="db-card ws-sidebar-card ws-sidebar-single-card" id="workspace-actions-card">
            <div className="ws-sidebar-top-actions">
              <button className="ws-action-btn ws-btn-primary" id="btn-take-quiz">
                <span className="ws-btn-icon">{Icon.play}</span> Take quiz
              </button>
              <button className="ws-action-btn ws-btn-secondary" id="btn-add-files">
                <span className="ws-btn-icon">{Icon.plus}</span> Add files
              </button>
              <button className="ws-action-btn ws-btn-secondary" id="btn-edit-files">
                <span className="ws-btn-icon">{Icon.edit}</span> Edit files
              </button>
              <button className="ws-action-btn ws-btn-secondary" id="btn-quiz-stats">
                <span className="ws-btn-icon">{Icon.stats}</span> Quiz stats for WS
              </button>
            </div>

            <div className="ws-sidebar-bottom-actions">
               <button 
                 className="ws-action-btn ws-btn-outline" 
                 id="btn-edit-workspace-name"
                 onClick={() => { setEditNameValue(workspaceName); setIsEditModalOpen(true); }}
               >
                 <span className="ws-btn-icon">{Icon.edit}</span> Edit name
               </button>
               <button 
                 className="ws-action-btn ws-btn-danger" 
                 id="btn-delete-workspace"
                 onClick={() => setIsDeleteModalOpen(true)}
               >
                 <span className="ws-btn-icon">{Icon.trash}</span> Delete workspace
               </button>
            </div>
          </section>

        </aside>
      </main>

      {/* ── Modals ── */}
      {isEditModalOpen && (
        <div className="ws-modal-overlay" id="edit-workspace-modal-overlay">
          <div className="ws-modal-card db-card" id="edit-workspace-modal">
            <h2 className="ws-modal-title">Edit Workspace Name</h2>
            <input 
              type="text" 
              className="ws-modal-input" 
              value={editNameValue} 
              onChange={(e) => setEditNameValue(e.target.value)}
              id="edit-workspace-name-input"
            />
            <div className="ws-modal-actions">
              <button 
                className="ws-action-btn ws-btn-outline" 
                onClick={() => setIsEditModalOpen(false)}
                id="btn-cancel-edit"
              >Cancel</button>
              <button 
                className="ws-action-btn ws-btn-primary" 
                onClick={() => { setWorkspaceName(editNameValue); setIsEditModalOpen(false); }}
                id="btn-save-edit"
              >Save</button>
            </div>
          </div>
        </div>
      )}

      {isDeleteModalOpen && (
        <div className="ws-modal-overlay" id="delete-workspace-modal-overlay">
          <div className="ws-modal-card db-card" id="delete-workspace-modal">
            <h2 className="ws-modal-title">Delete Workspace</h2>
            <p className="ws-modal-text">Are you sure you want to delete this workspace? This action cannot be undone.</p>
            <div className="ws-modal-actions">
              <button 
                className="ws-action-btn ws-btn-outline" 
                onClick={() => setIsDeleteModalOpen(false)}
                id="btn-cancel-delete"
              >Cancel</button>
              <button 
                className="ws-action-btn ws-btn-danger" 
                onClick={() => { setIsDeleted(true); setIsDeleteModalOpen(false); }}
                id="btn-confirm-delete"
              >Delete</button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
