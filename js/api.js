const API = {
    async getMentors() {
        await this.delay();
        // Return mock data for now, but could be stored in localStorage
        return {
            success: true,
            data: [
                { id: 1, name: 'Sarah Johnson', role: 'Senior Software Engineer', company: 'Google', expertise: ['React', 'Node.js', 'TypeScript', 'AWS'], rating: 4.9, sessions: 1245, hourlyRate: 85, responseTime: '< 30min', availability: 'available', bio: '10+ years at Google. Help engineers level up their careers and master frontend development.' },
                { id: 2, name: 'Michael Chen', role: 'Principal Data Scientist', company: 'Microsoft', expertise: ['Python', 'Machine Learning', 'TensorFlow', 'SQL'], rating: 4.8, sessions: 890, hourlyRate: 95, responseTime: '< 1hr', availability: 'available', bio: 'PhD in CS from Stanford. Help data scientists advance in ML and AI.' },
                { id: 3, name: 'Priya Patel', role: 'Lead UX Designer', company: 'Airbnb', expertise: ['Figma', 'User Research', 'Prototyping', 'Design Systems'], rating: 4.9, sessions: 756, hourlyRate: 75, responseTime: '< 30min', availability: 'busy', bio: 'Design lead at Airbnb. Passionate about mentoring aspiring designers.' },
                { id: 4, name: 'David Kim', role: 'DevOps Architect', company: 'Amazon', expertise: ['Docker', 'Kubernetes', 'AWS', 'CI/CD'], rating: 4.7, sessions: 532, hourlyRate: 90, responseTime: '< 2hrs', availability: 'available', bio: 'Infrastructure expert at AWS. Help teams build scalable cloud solutions.' },
                { id: 5, name: 'Emily Rodriguez', role: 'Engineering Manager', company: 'Meta', expertise: ['Leadership', 'Career Growth', 'System Design', 'Python'], rating: 4.9, sessions: 423, hourlyRate: 100, responseTime: '< 1hr', availability: 'available', bio: 'EM at Meta. Help engineers become tech leads and managers.' },
                { id: 6, name: 'James Wilson', role: 'Mobile Architect', company: 'Apple', expertise: ['iOS', 'Swift', 'SwiftUI', 'Objective-C'], rating: 4.8, sessions: 367, hourlyRate: 90, responseTime: '< 30min', availability: 'busy', bio: '10+ years iOS development. Help developers master Apple platforms.' },
                { id: 7, name: 'Lisa Zhang', role: 'Full Stack Developer', company: 'Netflix', expertise: ['React', 'Python', 'Django', 'PostgreSQL'], rating: 4.8, sessions: 289, hourlyRate: 70, responseTime: '< 1hr', availability: 'available', bio: 'Full stack developer at Netflix. Love teaching modern web development.' },
                { id: 8, name: 'Robert Taylor', role: 'Security Engineer', company: 'CrowdStrike', expertise: ['Cybersecurity', 'Penetration Testing', 'Network Security'], rating: 4.9, sessions: 178, hourlyRate: 95, responseTime: '< 2hrs', availability: 'available', bio: 'Security expert. Help teams build secure applications.' },
                { id: 9, name: 'Anna Kowalski', role: 'Product Manager', company: 'Spotify', expertise: ['Product Strategy', 'Agile', 'User Stories', 'Analytics'], rating: 4.7, sessions: 245, hourlyRate: 80, responseTime: '< 1hr', availability: 'busy', bio: 'PM at Spotify. Help aspiring PMs break into product.' },
                { id: 10, name: 'Carlos Mendez', role: 'Blockchain Developer', company: 'Coinbase', expertise: ['Solidity', 'Web3', 'Ethereum', 'Smart Contracts'], rating: 4.8, sessions: 156, hourlyRate: 110, responseTime: '< 30min', availability: 'available', bio: 'Blockchain expert. Help developers enter Web3 space.' },
                { id: 11, name: 'Nina Patel', role: 'Data Engineer', company: 'Uber', expertise: ['Spark', 'Kafka', 'Hadoop', 'Python'], rating: 4.7, sessions: 198, hourlyRate: 85, responseTime: '< 1hr', availability: 'available', bio: 'Data engineer at Uber. Help build scalable data pipelines.' },
                { id: 12, name: 'Tom Anderson', role: 'Game Developer', company: 'Unity', expertise: ['Unity', 'C#', 'Game Design', '3D Graphics'], rating: 4.8, sessions: 167, hourlyRate: 75, responseTime: '< 2hrs', availability: 'busy', bio: 'Game developer with 8+ years experience. Help create amazing games.' },
                { id: 13, name: 'Maria Garcia', role: 'QA Lead', company: 'Salesforce', expertise: ['Testing', 'Automation', 'Selenium', 'CI/CD'], rating: 4.6, sessions: 134, hourlyRate: 65, responseTime: '< 1hr', availability: 'available', bio: 'QA expert. Help teams implement robust testing strategies.' },
                { id: 14, name: 'Alex Kumar', role: 'Technical Writer', company: 'GitHub', expertise: ['Documentation', 'API Docs', 'Technical Writing', 'Markdown'], rating: 4.8, sessions: 98, hourlyRate: 60, responseTime: '< 30min', availability: 'available', bio: 'Technical writer at GitHub. Help developers write better docs.' },
                { id: 15, name: 'Sophie Williams', role: 'AR/VR Developer', company: 'Magic Leap', expertise: ['Unity', 'ARKit', 'ARCore', '3D Modeling'], rating: 4.9, sessions: 87, hourlyRate: 95, responseTime: '< 1hr', availability: 'busy', bio: 'AR/VR specialist. Help build immersive experiences.' }
            ]
        };
    },

    async getCourses() {
        await this.delay();
        // Get courses from localStorage or return default
        let courses = this.getStoredData('skillbridge_courses');
        if (!courses || courses.length === 0) {
            courses = [
                { id: 1, title: 'HTML & CSS Fundamentals', instructor: 'Sarah Johnson', duration: '4 weeks', rating: 4.8, students: 1250, price: 49 },
                { id: 2, title: 'JavaScript Mastery', instructor: 'Michael Chen', duration: '6 weeks', rating: 4.9, students: 890, price: 79 },
                { id: 3, title: 'React Development', instructor: 'Priya Patel', duration: '8 weeks', rating: 4.7, students: 756, price: 99 }
            ];
            this.saveData('skillbridge_courses', courses);
        }
        return { success: true, data: courses };
    },

    async getJobs() {
        await this.delay();
        // Get jobs from localStorage or return default
        let jobs = this.getStoredData('skillbridge_jobs');
        if (!jobs || jobs.length === 0) {
            jobs = [
                { id: 1, title: 'Frontend Developer', company: 'TechCorp', location: 'Remote', salary: '$70k-90k', type: 'Full-time' },
                { id: 2, title: 'Full Stack Engineer', company: 'StartupXYZ', location: 'San Francisco', salary: '$90k-120k', type: 'Full-time' },
                { id: 3, title: 'UI/UX Designer', company: 'DesignHub', location: 'New York', salary: '$60k-80k', type: 'Contract' }
            ];
            this.saveData('skillbridge_jobs', jobs);
        }
        return { success: true, data: jobs };
    },

    async getStudyGroups() {
        await this.delay();
        // Get study groups from localStorage or return default
        let groups = this.getStoredData('skillbridge_groups');
        if (!groups || groups.length === 0) {
            groups = [
                {
                    id: 1,
                    name: 'JavaScript Masters',
                    description: 'Master advanced JavaScript concepts',
                    category: 'programming',
                    language: 'JavaScript',
                    members: 25,
                    maxMembers: 30
                },
                {
                    id: 2,
                    name: 'React Developers',
                    description: 'Build modern React applications',
                    category: 'framework',
                    language: 'JavaScript',
                    members: 18,
                    maxMembers: 25
                }
            ];
            this.saveData('skillbridge_groups', groups);
        }
        return { success: true, data: groups };
    },

    // Helper methods for localStorage
    getStoredData(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    },

    saveData(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    },

    delay(ms = 500) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};
                members: 1234,
                online: 42,
                rating: 4.9,
                nextSession: 'Today 5pm'
            },
            {
                id: 2,
                name: 'Python Data Science',
                description: 'Learn data science with Python',
                category: 'data-science',
                language: 'Python',
                members: 892,
                online: 27,
                rating: 4.8,
                nextSession: 'Tomorrow 2pm'
            }
        ]
    };
}