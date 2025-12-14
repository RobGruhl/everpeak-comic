/**
 * Character and Location Gallery Logic
 */

class CharacterGallery {
    constructor() {
        this.characters = {};
        this.filter = 'all';
        this.mainParty = ['Val', 'Prismor', 'Apocalypse Winter', 'Lunara', 'Malrik'];
        this.creatures = [
            'Verdant Mephit', 'Gear Mephit', 'Starlight Mephit',
            'Blink Mephit', 'Melody Mephit', 'Sorrel - Dragon Form'
        ];
    }

    async init() {
        try {
            const response = await fetch('data/characters.json');
            if (!response.ok) {
                throw new Error('Failed to load characters data');
            }
            this.characters = await response.json();
            this.renderGallery();
            this.setupFilters();
            this.setupModal();
        } catch (error) {
            console.error('Failed to initialize character gallery:', error);
            this.showError('Failed to load character data. Please refresh the page.');
        }
    }

    categorizeCharacters() {
        return Object.entries(this.characters).map(([name, data]) => {
            let category = 'npcs';
            if (this.mainParty.includes(name)) {
                category = 'party';
            } else if (this.creatures.includes(name)) {
                category = 'creatures';
            }

            return {
                name,
                ...data,
                category
            };
        });
    }

    renderGallery() {
        const characters = this.categorizeCharacters();
        const filtered = this.filter === 'all' ? characters :
                        characters.filter(c => c.category === this.filter);

        const container = document.getElementById('character-grid');

        if (filtered.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <p>No characters found in this category.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = filtered.map(char => {
            const role = this.extractRole(char);
            const race = this.extractRace(char);
            const detailUrl = this.getDetailUrl(char);

            return `
                <div class="character-card" data-category="${char.category}">
                    <h3>${char.name}</h3>
                    ${role ? `<p class="role">${role}</p>` : ''}
                    ${race ? `<p class="race">${race}</p>` : ''}
                    ${detailUrl ?
                        `<a href="${detailUrl}" class="expand-btn">View Full Details</a>` :
                        `<button class="expand-btn" data-character="${char.name}">View Full Description</button>`
                    }
                </div>
            `;
        }).join('');

        // Add click handlers for cards without detail pages (fallback to modal)
        container.querySelectorAll('.expand-btn[data-character]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const charName = btn.dataset.character;
                this.showCharacterModal(charName);
            });
        });
    }

    getDetailUrl(char) {
        const urlMap = {
            // Main party characters
            'Val': 'characters/val.html',
            'Prismor': 'characters/prismor.html',
            'Apocalypse Winter': 'characters/apocalypse_winter.html',
            'Lunara': 'characters/lunara.html',
            'Malrik': 'characters/malrik.html',

            // NPCs
            'Sorrel - Halfling': 'npcs/sorrel_halfling.html',
            'Sorrel - Dragon Form': 'npcs/sorrel_dragon.html',
            'Marge': 'npcs/marge.html',
            'Barth': 'npcs/barth.html',
            'Marivielle Greenbough': 'npcs/marivielle.html',
            'Lord Alric': 'npcs/lord_alric.html',

            // Monsters/Creatures
            'Verdant Mephit': 'monsters/verdant_mephit.html',
            'Gear Mephit': 'monsters/gear_mephit.html',
            'Starlight Mephit': 'monsters/starlight_mephit.html',
            'Blink Mephit': 'monsters/blink_mephit.html',
            'Melody Mephit': 'monsters/melody_mephit.html'
        };

        return urlMap[char.name] || null;
    }

    extractRole(char) {
        if (!char.description_components) return '';

        // Try to find class information
        if (char.description_components.class) {
            return char.description_components.class;
        }

        // Try to extract from full description
        if (char.full_description) {
            const desc = char.full_description.toLowerCase();
            if (desc.includes('monk')) return 'Monk';
            if (desc.includes('paladin')) return 'Paladin';
            if (desc.includes('wizard')) return 'Wizard';
            if (desc.includes('druid')) return 'Druid';
            if (desc.includes('rogue')) return 'Rogue';
            if (desc.includes('librarian')) return 'Head Librarian';
            if (desc.includes('blacksmith')) return 'Blacksmith';
            if (desc.includes('dragon')) return 'Dragon';
        }

        return '';
    }

    extractRace(char) {
        if (!char.description_components) return '';

        if (char.description_components.race) {
            return char.description_components.race;
        }

        // Try to extract from full description
        if (char.full_description) {
            const desc = char.full_description.toLowerCase();
            if (desc.includes('brass dragonborn')) return 'Brass Dragonborn';
            if (desc.includes('crystal dragonborn')) return 'Crystal Dragonborn';
            if (desc.includes('high elf')) return 'High Elf';
            if (desc.includes('drow')) return 'Drow';
            if (desc.includes('human')) return 'Human';
            if (desc.includes('half-elf')) return 'Half-Elf';
            if (desc.includes('halfling')) return 'Halfling';
            if (desc.includes('gold dragon')) return 'Gold Dragon';
        }

        return '';
    }

    setupFilters() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Update filter and re-render
                this.filter = btn.dataset.filter;
                this.renderGallery();
            });
        });
    }

    setupModal() {
        const modal = document.getElementById('character-modal');

        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                modal.classList.remove('active');
            }
        });
    }

    showCharacterModal(name) {
        const char = this.characters[name];
        if (!char) return;

        const modal = document.getElementById('character-modal');

        modal.innerHTML = `
            <div class="modal-content">
                <button class="close-modal" aria-label="Close">&times;</button>
                <h2>${char.name}</h2>
                ${char.full_description ?
                    `<p class="description">${char.full_description}</p>` : ''}
                ${this.renderDescriptionComponents(char.description_components)}
            </div>
        `;

        modal.classList.add('active');

        // Add close button handler
        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    renderDescriptionComponents(components) {
        if (!components) return '';

        return Object.entries(components)
            .filter(([key, value]) => value && value.trim())
            .map(([key, value]) => `
                <div class="desc-section">
                    <h4>${this.formatComponentTitle(key)}</h4>
                    <p>${value}</p>
                </div>
            `).join('');
    }

    formatComponentTitle(key) {
        return key
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
    }

    showError(message) {
        const container = document.getElementById('character-grid');
        container.innerHTML = `
            <div class="error-message">
                <h2>Error</h2>
                <p>${message}</p>
            </div>
        `;
    }
}

class LocationGallery {
    constructor() {
        this.locations = {};
    }

    async init() {
        try {
            const response = await fetch('data/locations.json');
            if (!response.ok) {
                throw new Error('Failed to load locations data');
            }
            this.locations = await response.json();
            this.renderGallery();
            this.setupModal();
        } catch (error) {
            console.error('Failed to initialize location gallery:', error);
            this.showError('Failed to load location data. Please refresh the page.');
        }
    }

    renderGallery() {
        const container = document.getElementById('location-grid');
        const locations = Object.entries(this.locations);

        if (locations.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <p>No locations found.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = locations.map(([name, data]) => {
            const detailUrl = this.getDetailUrl(name);

            return `
                <div class="character-card location-card">
                    <h3>${data.name || name}</h3>
                    ${data.description_components?.type ?
                        `<p class="role">${data.description_components.type}</p>` : ''}
                    ${detailUrl ?
                        `<a href="${detailUrl}" class="expand-btn">View Full Details</a>` :
                        `<button class="expand-btn" data-location="${name}">View Full Description</button>`
                    }
                </div>
            `;
        }).join('');

        // Add click handlers for locations without detail pages (fallback to modal)
        container.querySelectorAll('.expand-btn[data-location]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const locName = btn.dataset.location;
                this.showLocationModal(locName);
            });
        });
    }

    getDetailUrl(locationName) {
        const urlMap = {
            'Everpeak Citadel Exterior': 'locations/everpeak_citadel_exterior.html',
            'Festival Marketplace': 'locations/festival_marketplace.html',
            'Grand Courtyard': 'locations/grand_courtyard.html',
            'The Grand Library': 'locations/the_grand_library.html',
            'The Observatory': 'locations/the_observatory.html',
            'Courier Tunnels': 'locations/courier_tunnels.html',
            'Balcony Garden Café': 'locations/balcony_garden_café.html',
            "Barth's Forge": 'locations/barths_forge.html',
            'Sled Race Course': 'locations/sled_race_course.html',
            'The Elven Sanctum': 'locations/the_elven_sanctum.html',
            'Mountain Path': 'locations/mountain_path.html'
        };

        return urlMap[locationName] || null;
    }

    setupModal() {
        const modal = document.getElementById('location-modal');

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                modal.classList.remove('active');
            }
        });
    }

    showLocationModal(name) {
        const loc = this.locations[name];
        if (!loc) return;

        const modal = document.getElementById('location-modal');

        modal.innerHTML = `
            <div class="modal-content">
                <button class="close-modal" aria-label="Close">&times;</button>
                <h2>${loc.name || name}</h2>
                ${loc.full_description ?
                    `<p class="description">${loc.full_description}</p>` : ''}
                ${this.renderDescriptionComponents(loc.description_components)}
            </div>
        `;

        modal.classList.add('active');

        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    renderDescriptionComponents(components) {
        if (!components) return '';

        return Object.entries(components)
            .filter(([key, value]) => value && value.trim())
            .map(([key, value]) => `
                <div class="desc-section">
                    <h4>${this.formatComponentTitle(key)}</h4>
                    <p>${value}</p>
                </div>
            `).join('');
    }

    formatComponentTitle(key) {
        return key
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
    }

    showError(message) {
        const container = document.getElementById('location-grid');
        container.innerHTML = `
            <div class="error-message">
                <h2>Error</h2>
                <p>${message}</p>
            </div>
        `;
    }
}

// Initialize based on page
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('character-grid')) {
        window.characterGallery = new CharacterGallery();
        window.characterGallery.init();
    } else if (document.getElementById('location-grid')) {
        window.locationGallery = new LocationGallery();
        window.locationGallery.init();
    }
});
