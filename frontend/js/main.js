class CertificadosSolanaPy {
    constructor() {
        this.currentPage = 'register';
        this.apiBaseUrl = 'http://localhost:8000';
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupWalletInfo();
        this.loadPage('register');
    }

    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const page = e.target.closest('.nav-item').getAttribute('data-page');
                this.navigateTo(page);
            });
        });
    }

    setupWalletInfo() {
        const walletBtn = document.getElementById('wallet-info-btn');
        walletBtn.addEventListener('click', () => {
            this.getWalletInfo();
        });
    }

    navigateTo(page) {
        // Update nav active state
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-page="${page}"]`).classList.add('active');

        // Update page visibility
        document.querySelectorAll('.page').forEach(pageEl => {
            pageEl.classList.remove('active');
        });
        document.getElementById(`${page}-page`).classList.add('active');

        this.currentPage = page;
        this.loadPage(page);
    }

    loadPage(page) {
        switch(page) {
            case 'register':
                this.loadRegisterPage();
                break;
            case 'verify':
                this.loadVerifyPage();
                break;
        }
    }

    loadRegisterPage() {
        const registerPage = document.getElementById('register-page');
        registerPage.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Registrar Certificado</h2>
                    <p class="card-subtitle">Registre um novo certificado na blockchain Solana</p>
                </div>
                
                <form id="register-form" class="register-form">
                    <div class="form-group">
                        <label class="form-label" for="event">Evento</label>
                        <input 
                            type="text" 
                            id="event" 
                            class="form-input" 
                            placeholder="Ex: PlythonFloripa 25/10/2025"
                            required
                        >
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label" for="name">Nome Completo</label>
                            <input 
                                type="text" 
                                id="name" 
                                class="form-input" 
                                placeholder="Digite o nome completo"
                                required
                            >
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="document">CPF</label>
                            <input 
                                type="text" 
                                id="document" 
                                class="form-input" 
                                placeholder="Apenas números"
                                required
                                maxlength="11"
                            >
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="duration_hours">Duração (horas)</label>
                        <input 
                            type="number" 
                            id="duration_hours" 
                            class="form-input" 
                            placeholder="Ex: 5"
                            required
                            min="1"
                        >
                    </div>

                    <div id="register-alert-container"></div>

                    <button type="submit" class="btn btn-primary btn-full" id="register-submit-btn">
                        <span></span>
                        Registrar na Blockchain
                    </button>
                </form>

                <div id="register-result-container"></div>
            </div>
        `;

        this.setupRegisterForm();
    }

    loadVerifyPage() {
        const verifyPage = document.getElementById('verify-page');
        verifyPage.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Verificar Certificado</h2>
                    <p class="card-subtitle">Verifique a autenticidade de um certificado registrado</p>
                </div>
                
                <form id="verify-form" class="verify-form">
                    <div class="form-group">
                        <label class="form-label" for="txid">Transaction ID (TXID)</label>
                        <input 
                            type="text" 
                            id="txid" 
                            class="form-input" 
                            placeholder="Ex: hgFQknAvNKzVTD6UzCoCc6yd9SZXCWoX7CZ4wZHtTyr6j41iivgrK5pNfqBtTLwFiFyanmqT79uvFtwPBiNfbyh"
                            required
                        >
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="verify-event">Evento</label>
                        <input 
                            type="text" 
                            id="verify-event" 
                            class="form-input" 
                            placeholder="Ex: PlythonFloripa 25/10/2025"
                            required
                        >
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label" for="verify-name">Nome Completo</label>
                            <input 
                                type="text" 
                                id="verify-name" 
                                class="form-input" 
                                placeholder="Digite o nome completo"
                                required
                            >
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="verify-document">CPF</label>
                            <input 
                                type="text" 
                                id="verify-document" 
                                class="form-input" 
                                placeholder="Apenas números"
                                required
                                maxlength="11"
                            >
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label" for="uuid">UUID</label>
                            <input 
                                type="text" 
                                id="uuid" 
                                class="form-input" 
                                placeholder="Ex: 173146f8-5a92-4f57-98ee-fd629f3a92a0"
                                required
                            >
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="verify-duration">Duração (horas)</label>
                            <input 
                                type="number" 
                                id="verify-duration" 
                                class="form-input" 
                                placeholder="Ex: 5"
                                required
                                min="1"
                            >
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="time">Timestamp</label>
                        <input 
                            type="text" 
                            id="time" 
                            class="form-input" 
                            placeholder="Ex: 2025-10-24T12:56:37.161876"
                            required
                        >
                    </div>

                    <div id="verify-alert-container"></div>

                    <button type="submit" class="btn btn-primary btn-full" id="verify-submit-btn">
                        <span></span>
                        Verificar Certificado
                    </button>
                </form>

                <div id="verify-result-container"></div>
            </div>
        `;

        this.setupVerifyForm();
    }

    setupRegisterForm() {
        const form = document.getElementById('register-form');
        const submitBtn = document.getElementById('register-submit-btn');

        // CPF formatting
        const documentInput = document.getElementById('document');
        documentInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '');
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span>Registrando...';
            
            this.clearAlerts('register-alert-container');
            this.clearResults('register-result-container');

            try {
                const certificateData = {
                    event: document.getElementById('event').value.trim(),
                    name: document.getElementById('name').value.trim(),
                    document: document.getElementById('document').value.trim(),
                    duration_hours: parseInt(document.getElementById('duration_hours').value)
                };

                const response = await this.registerCertificate(certificateData);
                
                if (response.status === 'sucesso') {
                    this.showAlert('register-alert-container', 'success', 'Certificado registrado com sucesso na blockchain!');
                    this.showRegisterResult(response);
                    form.reset();
                } else {
                    this.showAlert('register-alert-container', 'error', response.message || 'Erro ao registrar certificado');
                }
            } catch (error) {
                this.showAlert('register-alert-container', 'error', 'Erro de conexão com o servidor. Verifique se a API está rodando.');
                console.error('Register error:', error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<span></span>Registrar na Blockchain';
            }
        });
    }

    setupVerifyForm() {
        const form = document.getElementById('verify-form');
        const submitBtn = document.getElementById('verify-submit-btn');

        // CPF formatting
        const documentInput = document.getElementById('verify-document');
        documentInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '');
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading"></span>Verificando...';
            
            this.clearAlerts('verify-alert-container');
            this.clearResults('verify-result-container');

            try {
                const txid = document.getElementById('txid').value.trim();
                const verifyData = {
                    event: document.getElementById('verify-event').value.trim(),
                    uuid: document.getElementById('uuid').value.trim(),
                    name: document.getElementById('verify-name').value.trim(),
                    document: document.getElementById('verify-document').value.trim(),
                    duration_hours: parseInt(document.getElementById('verify-duration').value),
                    time: document.getElementById('time').value.trim()
                };

                const response = await this.verifyCertificate(txid, verifyData);
                
                if (response.status === 'sucesso') {
                    this.showAlert('verify-alert-container', 'success', 'Certificado verificado com sucesso!');
                    this.showVerifyResult(response);
                } else {
                    this.showAlert('verify-alert-container', 'error', response.message || 'Certificado não foi encontrado ou dados não conferem');
                    if (response.detalhes) {
                        this.showVerifyResult(response);
                    }
                }
            } catch (error) {
                this.showAlert('verify-alert-container', 'error', 'Erro de conexão com o servidor. Verifique se a API está rodando.');
                console.error('Verify error:', error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<span></span>Verificar Certificado';
            }
        });
    }

    async registerCertificate(data) {
        const response = await fetch(`${this.apiBaseUrl}/certificados/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async verifyCertificate(txid, data) {
        const response = await fetch(`${this.apiBaseUrl}/certificados/verify/${txid}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async getWalletInfo() {
        const walletBtn = document.getElementById('wallet-info-btn');
        const originalContent = walletBtn.innerHTML;
        
        walletBtn.disabled = true;
        walletBtn.innerHTML = '<span class="loading"></span>Carregando...';

        try {
            const response = await fetch(`${this.apiBaseUrl}/certificados/wallet-info`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.showWalletModal(data);
        } catch (error) {
            alert('Erro ao obter informações da carteira. Verifique se a API está rodando.');
            console.error('Wallet info error:', error);
        } finally {
            walletBtn.disabled = false;
            walletBtn.innerHTML = originalContent;
        }
    }

    showWalletModal(data) {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8); display: flex; align-items: center;
            justify-content: center; z-index: 1000; backdrop-filter: blur(5px);
        `;
        
        // Extract wallet info from nested response structure
        const wallet = data.carteira || {};
        const costs = data.custos || {};
        const instructions = data.instrucoes || {};
        
        const walletAddress = wallet.endereco || 'N/A';
        const network = wallet.rede || 'N/A';
        const balance = wallet.saldo_sol !== undefined ? wallet.saldo_sol.toFixed(6) : 'N/A';
        const mode = wallet.modo || 'N/A';
        const realTransactions = wallet.transacoes_reais ? 'Sim' : 'Não';
        
        modal.innerHTML = `
            <div style="background: var(--card-bg); border-radius: 24px; padding: 2rem; 
                        max-width: 600px; width: 90%; border: 1px solid var(--border-color);
                        box-shadow: var(--shadow-lg);">
                <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; font-size: 1.5rem;
                          background: var(--solana-gradient); -webkit-background-clip: text;
                          -webkit-text-fill-color: transparent; background-clip: text;">
                    💼 Informações da Carteira
                </h3>
                <div style="color: var(--text-secondary); line-height: 1.8; font-size: 0.95rem;">
                    <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color);">
                        <p style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Endereço:</strong></p>
                        <p style="word-break: break-all; font-family: monospace; font-size: 0.85em; background: rgba(255,255,255,0.05); padding: 0.5rem; border-radius: 6px; margin: 0;">${walletAddress}</p>
                    </div>
                    
                    <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color);">
                        <p style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Saldo:</strong> 
                            <span style="color: #00d4aa; font-weight: 600;">${balance} SOL</span>
                        </p>
                        <p style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Rede:</strong> 
                            <span style="text-transform: uppercase; color: #9945ff;">${network}</span>
                        </p>
                        <p style="margin-bottom: 0;"><strong style="color: var(--text-primary);">Modo:</strong> 
                            <span style="color: ${mode === 'simulacao' ? '#ffa500' : '#00d4aa'};">${mode}</span>
                        </p>
                    </div>
                    
                    <div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color);">
                        <p style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary);">Transações Reais:</strong> ${realTransactions}</p>
                        <p style="margin-bottom: 0;"><strong style="color: var(--text-primary);">Custo por Transação:</strong> ${costs.transacao_memo || 'N/A'}</p>
                    </div>
                    
                    ${instructions.obter_sol ? `
                    <div style="background: rgba(153, 69, 255, 0.1); padding: 0.75rem; border-radius: 8px; border-left: 3px solid #9945ff;">
                        <p style="margin: 0; font-size: 0.9em;"><strong>💡 Dica:</strong> ${instructions.obter_sol}</p>
                    </div>
                    ` : ''}
                </div>
                <button onclick="this.closest('.modal').remove()" 
                        style="margin-top: 1.5rem; background: var(--solana-gradient); 
                               color: white; border: none; padding: 0.75rem 1.5rem; 
                               border-radius: 8px; cursor: pointer; width: 100%; 
                               font-weight: 600; transition: opacity 0.2s; font-size: 1rem;"
                        onmouseover="this.style.opacity='0.9'"
                        onmouseout="this.style.opacity='1'">
                    Fechar
                </button>
            </div>
        `;
        
        modal.className = 'modal';
        modal.onclick = (e) => e.target === modal && modal.remove();
        document.body.appendChild(modal);
    }

    showRegisterResult(response) {
        const container = document.getElementById('register-result-container');
        const cert = response.certificado;
        const blockchain = response.blockchain;
        const jsonCanonical = cert.json_canonico || response.json_canonico;
        
        container.innerHTML = `
            <div class="result-card">
                <div class="result-header">
                    <h3 style="color: var(--text-primary);">Certificado Registrado</h3>
                    <span class="result-status success">✅ Sucesso</span>
                </div>
                
                <div class="result-field">
                    <div class="result-label">UUID</div>
                    <div class="result-value">${cert.uuid}</div>
                </div>
                
                <div class="result-field">
                    <div class="result-label">Hash SHA-256</div>
                    <div class="result-value" style="word-break: break-all; font-family: monospace;">${cert.hash_sha256}</div>
                </div>
                
                <div class="result-field">
                    <div class="result-label">Transaction ID</div>
                    <div class="result-value" style="word-break: break-all; font-family: monospace;">${cert.txid_solana}</div>
                </div>
                
                <div class="result-field">
                    <div class="result-label">Explorer Solana</div>
                    <div class="result-value">
                        <a href="${blockchain.explorer_url}" target="_blank" class="result-link">
                            🔗 Ver na Blockchain →
                        </a>
                    </div>
                </div>
                
                <div class="result-field">
                    <div class="result-label">Timestamp</div>
                    <div class="result-value">${cert.timestamp}</div>
                </div>
                
                ${jsonCanonical ? `
                <div class="result-field">
                    <div class="result-label">JSON Canônico</div>
                    <div class="result-value">
                        <pre style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; 
                                    overflow-x: auto; font-family: monospace; font-size: 0.85em; 
                                    margin: 0; border: 1px solid var(--border-color);">${JSON.stringify(jsonCanonical, null, 2)}</pre>
                    </div>
                </div>
                ` : ''}
            </div>
        `;
    }

    showVerifyResult(response) {
        const container = document.getElementById('verify-result-container');
        const isSuccess = response.status === 'sucesso';
        
        container.innerHTML = `
            <div class="result-card">
                <div class="result-header">
                    <h3 style="color: var(--text-primary);">Resultado da Verificação</h3>
                    <span class="result-status ${isSuccess ? 'success' : 'error'}">
                        ${isSuccess ? 'Válido' : 'Inválido'}
                    </span>
                </div>
                
                <div class="result-field">
                    <div class="result-label">Status</div>
                    <div class="result-value">${response.message || response.status}</div>
                </div>
                
                ${response.detalhes ? `
                    <div class="result-field">
                        <div class="result-label">Detalhes</div>
                        <div class="result-value">${JSON.stringify(response.detalhes, null, 2)}</div>
                    </div>
                ` : ''}
            </div>
        `;
    }

    showAlert(containerId, type, message) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <span>${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
            <span>${message}</span>
        `;
        container.appendChild(alert);
        
        // Auto remove after 8 seconds
        setTimeout(() => {
            alert.remove();
        }, 8000);
    }

    clearAlerts(containerId) {
        const container = document.getElementById(containerId);
        if (container) container.innerHTML = '';
    }

    clearResults(containerId) {
        const container = document.getElementById(containerId);
        if (container) container.innerHTML = '';
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CertificadosSolanaPy();
});
