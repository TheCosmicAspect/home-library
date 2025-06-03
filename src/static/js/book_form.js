document.addEventListener('DOMContentLoaded', function() {
    // Initialize Tom Select for all select fields
    const selects = document.querySelectorAll('.tom-select');
    let tomSelectInstances = {};
    
    selects.forEach(function(select) {
        tomSelectInstances[select.id] = new TomSelect(select, {
            plugins: ['remove_button', 'clear_button'],
            create: false,
            sortField: {
                field: "text",
                direction: "asc"
            },
            searchField: ['text'],
            placeholder: select.getAttribute('placeholder') || 'Search and select...',
            maxOptions: null,
            closeAfterSelect: !select.hasAttribute('multiple')
        });
    });

    // ISBN lookup functionality
    const isbnField = document.getElementById('isbn');
    const titleField = document.getElementById('title');
    const descriptionField = document.getElementById('description');
    const coverUrlField = document.getElementById('cover_url');
    let debounceTimer;

    isbnField.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const isbn = this.value.replace(/[-\s]/g, ''); // Remove hyphens and spaces
        
        if (isbn.length >= 10) {
            debounceTimer = setTimeout(() => fetchBookData(isbn), 500);
        }
    });

    async function fetchBookData(isbn) {
        try {
            showLoadingState(true);
            
            // Use your Flask route for server-side lookup
            const response = await fetch(`/api/isbn-lookup/${isbn}`);
            const data = await response.json();
            
            if (data.success) {
                autofillForm(data);
            } else {
                showMessage(`No book found for ISBN: ${isbn}`, 'warning');
            }
        } catch (error) {
            console.error('Error fetching book data:', error);
            showMessage('Error looking up ISBN. Please try again.', 'danger');
        } finally {
            showLoadingState(false);
        }
    }

    async function autofillForm(bookData) {
        // Fill title if empty
        if (bookData.title && !titleField.value) {
            titleField.value = bookData.title;
        }

        // Fill description if empty
        if (bookData.description && !descriptionField.value) {
            descriptionField.value = bookData.description;
        }

        // Fill cover URL if empty
        if (bookData.cover_url && !coverUrlField.value) {
            coverUrlField.value = bookData.cover_url;
        }

        // Handle authors - try to match existing authors or suggest creation
        if (bookData.authors && bookData.authors.length > 0) {
            await handleAuthors(bookData.authors);
        }

        // Handle categories as tags
        if (bookData.categories && bookData.categories.length > 0) {
            await handleTags(bookData.categories);
        }

        // Show success message
        showMessage('Book information loaded from ISBN!', 'success');
    }

    async function handleAuthors(bookAuthors) {
        const authorsSelect = tomSelectInstances['authors'];
        if (!authorsSelect) return;

        const existingOptions = authorsSelect.options;
        const matchedAuthors = [];
        const missingAuthors = [];

        bookAuthors.forEach(authorName => {
            // Try to find matching author in existing options
            const match = Object.values(existingOptions).find(option => 
                option.text.toLowerCase().includes(authorName.toLowerCase()) ||
                authorName.toLowerCase().includes(option.text.toLowerCase())
            );
            
            if (match) {
                matchedAuthors.push(match.value);
            } else {
                missingAuthors.push(authorName);
            }
        });

        // Set matched authors
        if (matchedAuthors.length > 0) {
            authorsSelect.setValue(matchedAuthors);
        }

        // Handle missing authors
        if (missingAuthors.length > 0) {
            showMissingAuthorsModal(missingAuthors);
        }
    }

    async function handleTags(categories) {
        const tagsSelect = tomSelectInstances['tags'];
        if (!tagsSelect) return;

        const existingOptions = tagsSelect.options;
        const matchedTags = [];
        const missingTags = [];

        categories.forEach(category => {
            // Try to find matching tag in existing options
            const match = Object.values(existingOptions).find(option => 
                option.text.toLowerCase().includes(category.toLowerCase()) ||
                category.toLowerCase().includes(option.text.toLowerCase())
            );
            
            if (match) {
                matchedTags.push(match.value);
            } else {
                missingTags.push(category);
            }
        });

        // Set matched tags
        if (matchedTags.length > 0) {
            tagsSelect.setValue(matchedTags);
        }

        // Handle missing tags
        if (missingTags.length > 0) {
            showMissingTagsModal(missingTags);
        }
    }

    function showMissingAuthorsModal(missingAuthors) {
        const modal = new bootstrap.Modal(document.getElementById('missingAuthorsModal'));
        const listContainer = document.getElementById('missingAuthorsList');
        
        listContainer.innerHTML = '';
        
        missingAuthors.forEach((authorName, index) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'missing-item';
            itemDiv.innerHTML = `
                <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" value="${authorName}" id="missingAuthor${index}" checked>
                    <label class="form-check-label" for="missingAuthor${index}">
                        Create "${authorName}"
                    </label>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label class="form-label">Name:</label>
                        <input type="text" class="form-control form-control-sm" value="${authorName}" data-field="name">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Biography (optional):</label>
                        <textarea class="form-control form-control-sm" rows="2" data-field="bio"></textarea>
                    </div>
                </div>
            `;
            listContainer.appendChild(itemDiv);
        });
        
        modal.show();
    }

    function showMissingTagsModal(missingTags) {
        const modal = new bootstrap.Modal(document.getElementById('missingTagsModal'));
        const listContainer = document.getElementById('missingTagsList');
        
        listContainer.innerHTML = '';
        
        missingTags.forEach((tagName, index) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'missing-item';
            itemDiv.innerHTML = `
                <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" value="${tagName}" id="missingTag${index}" checked>
                    <label class="form-check-label" for="missingTag${index}">
                        Create "${tagName}"
                    </label>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label class="form-label">Label:</label>
                        <input type="text" class="form-control form-control-sm" value="${tagName}" data-field="label">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Description (optional):</label>
                        <textarea class="form-control form-control-sm" rows="2" data-field="description"></textarea>
                    </div>
                </div>
            `;
            listContainer.appendChild(itemDiv);
        });
        
        modal.show();
    }

    // Add Author functionality
    document.getElementById('saveAuthorBtn').addEventListener('click', async function() {
        const name = document.getElementById('authorName').value.trim();
        const bio = document.getElementById('authorBio').value.trim();
        
        if (!name) {
            alert('Please enter an author name.');
            return;
        }
        
        try {
            const response = await fetch('/api/authors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, bio })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add to Tom Select dropdown
                const authorsSelect = tomSelectInstances['authors'];
                authorsSelect.addOption({ value: data.author.id, text: data.author.name });
                authorsSelect.addItem(data.author.id);
                
                // Clear form and close modal
                document.getElementById('addAuthorForm').reset();
                bootstrap.Modal.getInstance(document.getElementById('addAuthorModal')).hide();
                
                showMessage(`Author "${name}" added successfully!`, 'success');
            } else {
                alert('Error adding author: ' + (data.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error adding author:', error);
            alert('Error adding author. Please try again.');
        }
    });

    // Add Tag functionality
    document.getElementById('saveTagBtn').addEventListener('click', async function() {
        const label = document.getElementById('tagLabel').value.trim();
        const description = document.getElementById('tagDescription').value.trim();
        
        if (!label) {
            alert('Please enter a tag label.');
            return;
        }
        
        try {
            const response = await fetch('/api/tags', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ label, description })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add to Tom Select dropdown
                const tagsSelect = tomSelectInstances['tags'];
                tagsSelect.addOption({ value: data.tag.id, text: data.tag.label });
                tagsSelect.addItem(data.tag.id);
                
                // Clear form and close modal
                document.getElementById('addTagForm').reset();
                bootstrap.Modal.getInstance(document.getElementById('addTagModal')).hide();
                
                showMessage(`Tag "${label}" added successfully!`, 'success');
            } else {
                alert('Error adding tag: ' + (data.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error adding tag:', error);
            alert('Error adding tag. Please try again.');
        }
    });

    // Create Missing Authors functionality
    document.getElementById('createMissingAuthorsBtn').addEventListener('click', async function() {
        const modal = document.getElementById('missingAuthorsModal');
        const checkedItems = modal.querySelectorAll('input[type="checkbox"]:checked');
        const authorsToCreate = [];
        
        checkedItems.forEach(checkbox => {
            const itemDiv = checkbox.closest('.missing-item');
            const name = itemDiv.querySelector('[data-field="name"]').value.trim();
            const bio = itemDiv.querySelector('[data-field="bio"]').value.trim();
            
            if (name) {
                authorsToCreate.push({ name, bio });
            }
        });
        
        if (authorsToCreate.length === 0) {
            bootstrap.Modal.getInstance(modal).hide();
            return;
        }
        
        try {
            const response = await fetch('/api/authors/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ authors: authorsToCreate })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const authorsSelect = tomSelectInstances['authors'];
                const newAuthorIds = [];
                
                data.authors.forEach(author => {
                    authorsSelect.addOption({ value: author.id, text: author.name });
                    newAuthorIds.push(author.id);
                });
                
                // Select all newly created authors
                authorsSelect.setValue([...authorsSelect.getValue(), ...newAuthorIds]);
                
                bootstrap.Modal.getInstance(modal).hide();
                showMessage(`${data.authors.length} author(s) created successfully!`, 'success');
            } else {
                alert('Error creating authors: ' + (data.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error creating authors:', error);
            alert('Error creating authors. Please try again.');
        }
    });

    // Create Missing Tags functionality
    document.getElementById('createMissingTagsBtn').addEventListener('click', async function() {
        const modal = document.getElementById('missingTagsModal');
        const checkedItems = modal.querySelectorAll('input[type="checkbox"]:checked');
        const tagsToCreate = [];
        
        checkedItems.forEach(checkbox => {
            const itemDiv = checkbox.closest('.missing-item');
            const label = itemDiv.querySelector('[data-field="label"]').value.trim();
            const description = itemDiv.querySelector('[data-field="description"]').value.trim();
            
            if (label) {
                tagsToCreate.push({ label, description });
            }
        });
        
        if (tagsToCreate.length === 0) {
            bootstrap.Modal.getInstance(modal).hide();
            return;
        }
        
        try {
            const response = await fetch('/api/tags/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ tags: tagsToCreate })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const tagsSelect = tomSelectInstances['tags'];
                const newTagIds = [];
                
                data.tags.forEach(tag => {
                    tagsSelect.addOption({ value: tag.id, text: tag.label });
                    newTagIds.push(tag.id);
                });
                
                // Select all newly created tags
                tagsSelect.setValue([...tagsSelect.getValue(), ...newTagIds]);
                
                bootstrap.Modal.getInstance(modal).hide();
                showMessage(`${data.tags.length} tag(s) created successfully!`, 'success');
            } else {
                alert('Error creating tags: ' + (data.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error creating tags:', error);
            alert('Error creating tags. Please try again.');
        }
    });

    function showLoadingState(isLoading) {
        const isbnField = document.getElementById('isbn');
        if (isLoading) {
            isbnField.style.background = 'linear-gradient(90deg, #f8f9fa 25%, transparent 25%, transparent 50%, #f8f9fa 50%, #f8f9fa 75%, transparent 75%, transparent) repeat-x';
            isbnField.style.backgroundSize = '20px 20px';
            isbnField.style.animation = 'loading 1s linear infinite';
        } else {
            isbnField.style.background = '';
            isbnField.style.animation = '';
        }
    }

    function showMessage(message, type = 'info') {
        // Create or update message div
        let messageDiv = document.getElementById('isbn-message');
        if (!messageDiv) {
            messageDiv = document.createElement('div');
            messageDiv.id = 'isbn-message';
            messageDiv.className = 'mt-2 p-2 rounded';
            isbnField.parentNode.appendChild(messageDiv);
        }
        
        messageDiv.className = `mt-2 p-2 rounded alert alert-${type === 'success' ? 'success' : type === 'info' ? 'info' : 'warning'}`;
        messageDiv.textContent = message;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }
});

// Add CSS for loading animation
const style = document.createElement('style');
style.textContent = `
    @keyframes loading {
        0% { background-position: 0 0; }
        100% { background-position: 20px 0; }
    }
`;
document.head.appendChild(style);