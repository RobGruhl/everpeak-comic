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
            const thumbnail = this.getThumbnail(char);
            const summary = this.getSummary(char);

            return `
                <div class="character-card" data-category="${char.category}">
                    ${thumbnail ? `<img src="${thumbnail}" alt="${char.name}" class="card-thumbnail" onerror="this.src='images/placeholder.png'">` : ''}
                    <div class="card-content">
                        <h3>${char.name}</h3>
                        ${role ? `<p class="role">${role}</p>` : ''}
                        ${race ? `<p class="race">${race}</p>` : ''}
                        ${summary ? `<p class="summary">${summary}</p>` : ''}
                        ${detailUrl ?
                            `<a href="${detailUrl}" class="expand-btn">View Full Details</a>` :
                            `<button class="expand-btn" data-character="${char.name}">View Full Description</button>`
                        }
                    </div>
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

    getThumbnail(char) {
        const thumbnailMap = {
            // Main party characters
            'Val': 'images/characters/val-portrait.png',
            'Prismor': 'images/characters/prismor-portrait.png',
            'Apocalypse Winter': 'images/characters/apocalypse-winter-portrait.png',
            'Lunara': 'images/characters/lunara-portrait.png',
            'Malrik': 'images/characters/malrik-portrait.png',

            // NPCs
            'Sorrel - Halfling': 'images/npcs/sorrel-halfling-portrait.png',
            'Sorrel - Dragon Form': 'images/npcs/sorrel-dragon-portrait.png',
            'Marge': 'images/npcs/marge-portrait.png',
            'Barth': 'images/npcs/barth-portrait.png',
            'Marivielle Greenbough': 'images/npcs/marivielle-portrait.png',
            'Lord Alric': 'images/npcs/lord-alric-portrait.png',

            // Monsters/Creatures
            'Verdant Mephit': 'images/monsters/verdant-mephit.png',
            'Gear Mephit': 'images/monsters/gear-mephit.png',
            'Starlight Mephit': 'images/monsters/starlight-mephit.png',
            'Blink Mephit': 'images/monsters/blink-mephit.png',
            'Melody Mephit': 'images/monsters/melody-mephit.png',

            // Background NPCs
            'Fantasy Crowd': 'images/npcs/fantasy-crowd.png',
            'Festival crowd': 'images/npcs/festival-crowd.png',
            'Halfling courier': 'images/npcs/halfling-courier.png',
            'Gambler': 'images/npcs/gambler.png',
            'Well-dressed gambler': 'images/npcs/gambler.png',
            'Race contestants': 'images/npcs/race-contestants.png'
        };

        return thumbnailMap[char.name] || null;
    }

    getSummary(char) {
        const summaryMap = {
            // Main party characters
            'Val': 'Friendly brass dragonborn courier and monk who delivers messages throughout Everpeak Citadel.',
            'Prismor': 'Noble blue crystal dragonborn paladin, veteran defender of Everpeak and mentor to younger settlers.',
            'Apocalypse Winter': 'Young human wizard and scholar obsessed with uncovering the mysteries of the Dawn\'s Crown alignment.',
            'Lunara': 'Ancient high elf druid who tends Everpeak\'s magical gardens and maintains Nature Essence balance.',
            'Malrik': 'Charming drow rogue and street performer who found acceptance and purpose in Everpeak.',

            // NPCs
            'Sorrel - Halfling': 'Curious "halfling child" who observes the party with unusual wisdom. Secretly a gold dragon wyrmling.',
            'Sorrel - Dragon Form': 'Small but majestic gold dragon wyrmling, ancient guardian testing the party\'s worth.',
            'Marge': 'Kindly head librarian and keeper of Everpeak\'s incomplete historical records.',
            'Barth': 'Stoic drow blacksmith troubled by theft of mysterious frozen iron from his forge.',
            'Marivielle Greenbough': 'Nurturing half-elf café owner who maintains an impossible garden oasis.',
            'Lord Alric': 'Ambitious noble antagonist seeking to control Mechanistic Essence for personal dominance.',

            // Monsters/Creatures
            'Verdant Mephit': 'Small nature elemental composed of vines, leaves, and thorny branches. Appears when Nature Essence is disturbed.',
            'Gear Mephit': 'Tiny mechanical imp of interlocking gears and metal plates. Manifests from disrupted Mechanistic Essence.',
            'Starlight Mephit': 'Luminous ethereal figure of swirling star-fields and cosmic dust. Emerges when Celestial Essence is disturbed.',
            'Blink Mephit': 'Nearly invisible creature that flickers like a mirage. Haunts areas with disrupted Displacement Essence.',
            'Melody Mephit': 'Pastel swirl of colored sound waves. Appears when Harmony Essence is corrupted.',

            // Background NPCs
            'Fantasy Crowd': 'Diverse gathering of fantasy races at the marketplace - elves, dwarves, humans, halflings, and dragonborn.',
            'Festival crowd': 'Large festive crowd celebrating the winter festival with decorations, laughter, and magical lighting.',
            'Halfling courier': 'Energetic young halfling messenger, fellow member of the courier guild, breathless with urgent news.',
            'Gambler': 'Well-dressed merchant willing to make friendly wagers during festival celebrations.',
            'Well-dressed gambler': 'Well-dressed merchant willing to make friendly wagers during festival celebrations.',
            'Race contestants': 'Athletic competitors preparing for the traditional Everpeak sled race down mountain slopes.'
        };

        return summaryMap[char.name] || '';
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
            const thumbnail = this.getThumbnail(name);
            const summary = this.getSummary(name);

            return `
                <div class="character-card location-card">
                    ${thumbnail ? `<img src="${thumbnail}" alt="${data.name || name}" class="card-thumbnail" onerror="this.src='images/placeholder.png'">` : ''}
                    <div class="card-content">
                        <h3>${data.name || name}</h3>
                        ${data.description_components?.type ?
                            `<p class="role">${data.description_components.type}</p>` : ''}
                        ${summary ? `<p class="summary">${summary}</p>` : ''}
                        ${detailUrl ?
                            `<a href="${detailUrl}" class="expand-btn">View Full Details</a>` :
                            `<button class="expand-btn" data-location="${name}">View Full Description</button>`
                        }
                    </div>
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

    getThumbnail(locationName) {
        const thumbnailMap = {
            'Everpeak Citadel Exterior': 'images/locations/everpeak_citadel_exterior.png',
            'Festival Marketplace': 'images/locations/festival_marketplace.png',
            'Grand Courtyard': 'images/locations/grand_courtyard.png',
            'The Grand Library': 'images/locations/the_grand_library.png',
            'The Observatory': 'images/locations/the_observatory.png',
            'Courier Tunnels': 'images/locations/courier_tunnels.png',
            'Balcony Garden Café': 'images/locations/balcony_garden_café.png',
            "Barth's Forge": 'images/locations/barths_forge.png',
            'Sled Race Course': 'images/locations/sled_race_course.png',
            'The Elven Sanctum': 'images/locations/the_elven_sanctum.png',
            'Mountain Path': 'images/locations/mountain_path.png'
        };

        return thumbnailMap[locationName] || null;
    }

    getSummary(locationName) {
        const summaryMap = {
            'Everpeak Citadel Exterior': 'Massive white stone fortress built atop converging ley lines with crystalline towers and ancient high elven architecture.',
            'Festival Marketplace': 'Bustling marketplace filled with vendors, decorations, and diverse fantasy races celebrating the winter festival.',
            'Grand Courtyard': 'Majestic ceremonial center of the citadel where important gatherings and the Yule Tree ceremony take place.',
            'The Grand Library': 'Scholar\'s paradise containing ancient knowledge about Everpeak\'s history and the high elves\' sacrifice.',
            'The Observatory': 'Intimate stargazing chamber with a magical telescope, recently restored and holding clues about the Dawn\'s Crown.',
            'Courier Tunnels': 'Maze-like passages beneath the citadel marked with chalk runes and displacement magic. Evidence of tampering.',
            'Balcony Garden Café': 'Impossible sunny terrace infused with Nature Essence, creating a warm oasis high in the snowy mountains.',
            "Barth's Forge": 'Hot working forge where Mechanistic Essence is harnessed for metalworking. Site of mysterious frozen iron theft.',
            'Sled Race Course': 'Dramatic mountain slope starting line showcasing Everpeak\'s festive spirit and breathtaking vistas.',
            'The Elven Sanctum': 'Hidden cavern containing the massive Orrery that controls elemental essence flows throughout the citadel.',
            'Mountain Path': 'Steep winding trail approach to Everpeak Citadel through snow-covered peaks and hardy pine forests.'
        };

        return summaryMap[locationName] || '';
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
