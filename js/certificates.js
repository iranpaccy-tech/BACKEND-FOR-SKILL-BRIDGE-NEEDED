const Certificates = {
    list: [],

    init() {
        this.loadCertificates();
    },

    async loadCertificates() {
        try {
            const response = await fetch('/api/certificates');
            const data = await response.json();
            if (data.success) {
                this.list = data.data;
                this.renderCertificates();
            }
        } catch (error) {
            console.error('Error loading certificates:', error);
        }
    },

    renderCertificates() {
        const container = document.getElementById('certificatesGrid');
        if (!container) return;

        if (this.list.length === 0) {
            container.innerHTML = `
                <div class="no-certificates">
                    <div class="no-certificates-icon">📄</div>
                    <h2>No Certificates</h2>
                    <p>You haven't earned any certificates yet. Complete courses to get started!</p>
                    <button class="btn-primary" onclick="Certificates.showAddForm()">Add Sample Certificate</button>
                </div>
            `;
            return;
        }

        container.innerHTML = this.list.map(c => `
            <div class="certificate-card">
                <h3>${c.title}</h3>
                <p>Issued: ${c.date}</p>
                <p>ID: ${c.credential}</p>
                <div class="certificate-actions">
                    <button class="btn-outline" onclick="Certificates.download(${c.id})">Download PDF</button>
                    <button class="btn-link" onclick="Certificates.share(${c.id})">Share</button>
                    <button class="btn-link" onclick="Certificates.edit(${c.id})">Edit</button>
                    <button class="btn-link" onclick="Certificates.delete(${c.id})">Delete</button>
                </div>
            </div>
        `).join('');
    },

    async addCertificate(title, date, credential) {
        try {
            const response = await fetch('/api/certificates', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, date, credential })
            });
            const data = await response.json();
            if (data.success) {
                this.list.push(data.certificate);
                this.renderCertificates();
                UI.showToast('Certificate added successfully!', 'success');
            }
        } catch (error) {
            console.error('Error adding certificate:', error);
            UI.showToast('Error adding certificate', 'error');
        }
    },

    async edit(id) {
        const cert = this.list.find(c => c.id === id);
        if (!cert) return;

        const newTitle = prompt('Enter new title:', cert.title);
        if (newTitle === null) return;

        const newDate = prompt('Enter new date (YYYY-MM-DD):', cert.date);
        if (newDate === null) return;

        const newCredential = prompt('Enter new credential ID:', cert.credential);
        if (newCredential === null) return;

        try {
            const response = await fetch(`/api/certificates/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTitle, date: newDate, credential: newCredential })
            });
            const data = await response.json();
            if (data.success) {
                Object.assign(cert, data.certificate);
                this.renderCertificates();
                UI.showToast('Certificate updated!', 'success');
            }
        } catch (error) {
            console.error('Error updating certificate:', error);
            UI.showToast('Error updating certificate', 'error');
        }
    },

    async delete(id) {
        if (!confirm('Are you sure you want to delete this certificate?')) return;

        try {
            const response = await fetch(`/api/certificates/${id}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (data.success) {
                this.list = this.list.filter(c => c.id !== id);
                this.renderCertificates();
                UI.showToast('Certificate deleted!', 'info');
            }
        } catch (error) {
            console.error('Error deleting certificate:', error);
            UI.showToast('Error deleting certificate', 'error');
        }
    },

    showAddForm() {
        // For demo, add a sample certificate
        this.addCertificate('Sample Certificate', new Date().toISOString().split('T')[0], 'CERT-' + Date.now());
    },

    async download(id) {
        try {
            const response = await fetch(`/api/certificates/${id}/download`);
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `certificate_${id}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                UI.showToast('Download complete!', 'success');
            } else {
                UI.showToast('Download failed', 'error');
            }
        } catch (error) {
            console.error('Error downloading certificate:', error);
            UI.showToast('Download failed', 'error');
        }
    },

    share(id) {
        const cert = this.list.find(c => c.id === id);
        if (!cert) return;

        UI.showToast('Certificate link copied!', 'success');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('certificates')) {
        Certificates.init();
    }
});