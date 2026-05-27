from typing import Dict, List, Any, Set

# Role configurations with required skills
ROLE_PROFILES = {
    "Backend Software Engineer": {
        "skills": ["Python", "Java", "Go", "C#", "Django", "Flask", "FastAPI", "Spring Boot", "REST APIs", "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "AWS", "Docker", "Git", "Microservices"],
        "category": "Backend Development",
        "description": "Designs and builds the server-side logic, database structures, APIs, and background processes of web applications.",
        "insights": {
            "avg_salary": "$135,000",
            "skills_in_demand": ["Go", "System Design", "Microservices", "Kubernetes", "PostgreSQL"],
            "growth_trend": "+18% (High Growth)"
        }
    },
    "Frontend React Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular", "Vue", "TailwindCSS", "Bootstrap", "Next.js", "Redux", "Git", "REST APIs"],
        "category": "Frontend Development",
        "description": "Translates UI/UX designs into responsive, accessible, and high-performance interactive interfaces for web applications.",
        "insights": {
            "avg_salary": "$115,000",
            "skills_in_demand": ["Next.js", "TypeScript", "TailwindCSS", "State Management", "Web Performance"],
            "growth_trend": "+15% (Steady Demand)"
        }
    },
    "Full Stack Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "TypeScript", "React", "Node.js", "Express", "REST APIs", "SQL", "PostgreSQL", "MongoDB", "Git", "Docker", "AWS", "Next.js"],
        "category": "Full Stack Development",
        "description": "Handles both server-side logic and front-end interface development, managing the complete end-to-end flow of applications.",
        "insights": {
            "avg_salary": "$125,000",
            "skills_in_demand": ["Node.js", "React", "AWS", "Docker", "Next.js"],
            "growth_trend": "+22% (Very High Growth)"
        }
    },
    "Data Scientist": {
        "skills": ["Python", "R", "Machine Learning", "Deep Learning", "Statistics", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "SQL", "Tableau", "Data Visualization", "Data Analytics"],
        "category": "Data Science & AI",
        "description": "Analyzes complex raw datasets, runs advanced statistical models, and extracts actionable insights using machine learning.",
        "insights": {
            "avg_salary": "$140,000",
            "skills_in_demand": ["Python", "Machine Learning", "SQL", "Statistical Modeling", "Tableau"],
            "growth_trend": "+25% (High Growth)"
        }
    },
    "AI/ML Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing", "Computer Vision", "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "NumPy", "LLMs", "Hugging Face", "Docker", "Git"],
        "category": "Data Science & AI",
        "description": "Designs, develops, and deploys scalable neural networks and machine learning models (NLP, Vision, LLMs) into production systems.",
        "insights": {
            "avg_salary": "$155,000",
            "skills_in_demand": ["PyTorch", "LLMs", "NLP", "Transformers", "Model Deployment (MLOps)"],
            "growth_trend": "+35% (Exponential Growth)"
        }
    },
    "Data Analyst": {
        "skills": ["SQL", "Excel", "Python", "Pandas", "Tableau", "PowerBI", "Data Visualization", "Data Analytics", "Statistics"],
        "category": "Data Analytics & BI",
        "description": "Performs descriptive analysis, builds business dashboards, and queries relational databases to deliver strategic business answers.",
        "insights": {
            "avg_salary": "$90,000",
            "skills_in_demand": ["SQL", "Excel", "PowerBI", "Python", "Data Visualization"],
            "growth_trend": "+12% (Steady)"
        }
    },
    "Cloud DevOps Engineer": {
        "skills": ["AWS", "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD", "Jenkins", "GitHub Actions", "Linux", "Bash Scripting", "Git", "Nginx"],
        "category": "DevOps & Cloud Infrastructure",
        "description": "Automates deployment pipelines, provisions secure cloud environments, and maintains infrastructure scalability and uptime.",
        "insights": {
            "avg_salary": "$145,000",
            "skills_in_demand": ["Kubernetes", "Terraform", "AWS", "CI/CD pipelines", "Docker"],
            "growth_trend": "+28% (High Growth)"
        }
    },
    "Mobile App Developer": {
        "skills": ["Flutter", "React Native", "Swift", "Kotlin", "Java", "iOS Development", "Android Development", "Android Studio", "Git", "REST APIs"],
        "category": "Mobile Application Development",
        "description": "Builds, tests, and deploys high-performance native or cross-platform mobile applications for iOS and Android devices.",
        "insights": {
            "avg_salary": "$120,000",
            "skills_in_demand": ["Flutter", "React Native", "Swift", "Kotlin", "Mobile CI/CD"],
            "growth_trend": "+14% (Stable)"
        }
    }
}

# Curated Learning Resources and Steps for specific skills
# ... [rest remains unchanged, we only modified from lines 4 to 123 in original, let's keep recommend_jobs update here too]
# Wait, let's include the recommend_jobs change in the same replacement block.
# Let's write the recommend_jobs code here as well.


# Curated Learning Resources and Steps for specific skills
LEARNING_PATHWAYS = {
    # Programming Languages
    "python": "🐍 **Python**: Complete 'Python for Everybody' (Coursera) or study official docs. Practice data structures, OOP, and decorators.",
    "java": "☕ **Java**: Master core Java concepts (Collections, Multithreading, OOP) on platforms like Udemy, and practice coding on LeetCode.",
    "go": "🐹 **Go (Golang)**: Go through 'A Tour of Go' and build microservices with Goroutines and Channels.",
    "rust": "🦀 **Rust**: Read 'The Rust Programming Language' book and build CLI tools to master memory safety and borrowing.",
    "typescript": "📘 **TypeScript**: Study TypeScript handbook, understand interfaces, generics, types, and migrate a vanilla JS project to TS.",
    
    # Web Development
    "react": "⚛️ **React**: Build 5 single-page apps using hooks, context API, and routing. Take 'React - The Complete Guide' (Academind/Udemy).",
    "next.js": "🌐 **Next.js**: Master Server-Side Rendering (SSR), Static Site Generation (SSG), and API routes through the official Next.js dashboard tutorial.",
    "node.js": "🟢 **Node.js**: Learn event loops, streams, and construct backend services using Express and PostgreSQL.",
    "django": "🎸 **Django**: Build robust full-stack or REST APIs using Django and Django Rest Framework (DRF) with built-in admin panels.",
    "fastapi": "⚡ **FastAPI**: Implement asynchronous REST endpoints, utilize Pydantic for validation, and deploy APIs with auto-generated Swagger documentation.",
    
    # Databases
    "sql": "🗄️ **SQL**: Learn joins, subqueries, CTEs, indexing, and window functions on SQLZoo, LeetCode, or DataCamp.",
    "postgresql": "🐘 **PostgreSQL**: Master database design, indexing strategies, stored procedures, and optimization of complex relational query execution plans.",
    "mongodb": "🍃 **MongoDB**: Study NoSQL document concepts, aggregation pipelines, and schema modeling for dynamic data objects.",
    "redis": "⚡ **Redis**: Learn in-memory caching mechanisms, pub/sub communication, and data structures (lists, hashes, sets).",
    
    # AI/ML & Data Science
    "machine learning": "🤖 **Machine Learning**: Study Andrew Ng's 'Machine Learning Specialization' on Coursera. Practice with Scikit-learn (regression, classification, clustering).",
    "deep learning": "🧠 **Deep Learning**: Complete DeepLearning.AI specialization. Learn CNNs, RNNs, and Transformers.",
    "tensorflow": "🍊 **TensorFlow**: Earn the TensorFlow Developer Certificate. Practice training neural networks for vision and NLP applications.",
    "pytorch": "🔥 **PyTorch**: Go through official PyTorch tutorials, implement papers, and build models using PyTorch Lightning.",
    "nlp": "🗣️ **NLP (Natural Language Processing)**: Learn word embeddings (Word2Vec, GloVe), Recurrent Neural Networks, and Hugging Face Transformers for sentiment analysis and text generation.",
    "llms": "🤖 **LLMs & GenAI**: Build retrieval-augmented generation (RAG) applications using LangChain, Hugging Face, OpenAI APIs, and Vector Databases (Chroma/Pinecone).",
    "tableau": "📊 **Tableau**: Learn to connect data sources, design interactive maps/dashboards, and tell visual business stories using Tableau Desktop.",
    "pandas": "🐼 **Pandas**: Master indexing, grouping, merging, cleaning, and aggregating dataframes inside Jupyter Notebooks.",
    
    # DevOps & Cloud
    "aws": "☁️ **AWS**: Prepare for the AWS Certified Solutions Architect Associate exam. Practice deploying containerized apps using ECS/EKS and serverless with Lambda.",
    "docker": "🐳 **Docker**: Learn to containerize applications, build efficient multi-stage Dockerfiles, and orchestrate environments using Docker Compose.",
    "kubernetes": "☸️ **Kubernetes**: Understand Pods, Services, Deployments, ConfigMaps, and prepare for the Certified Kubernetes Administrator (CKA) exam.",
    "terraform": "🛠️ **Terraform**: Learn Infrastructure as Code (IaC). Practice provisioning AWS or GCP resources using Terraform modules and state management.",
    "ci/cd": "🔄 **CI/CD**: Build automated pipelines (build, test, lint, deploy) using GitHub Actions, GitLab CI, or Jenkins.",
    
    # Software Engineering
    "system design": "📐 **System Design**: Read 'Designing Data-Intensive Applications' by Martin Kleppmann and study common architectures (load balancers, CDNs, sharding).",
    "data structures": "📊 **Data Structures & Algorithms**: Master Arrays, Linked Lists, Trees, Graphs, Sorting, Searching, and Dynamic Programming. Solve 150+ LeetCode problems.",
    "dsa": "📊 **Data Structures & Algorithms (DSA)**: Practice recursion, trees, graphs, sorting, searching, and dynamic programming. Solve standard interview sheets (Striver/Love Babbar).",
    "microservices": "🧩 **Microservices**: Understand service discovery (Consul/Eureka), API Gateways, event-driven messaging (Kafka/RabbitMQ), and distributed tracing."
}

def recommend_jobs(extracted_skills: List[str]) -> Dict[str, Any]:
    """
    Recommend jobs and estimate skill gaps based on the user's extracted skills.
    
    Returns:
        Dict: Recommendations, skill gaps, learning pathways, and predicted primary category.
    """
    user_skills_set = {s.lower() for s in extracted_skills}
    recommendations = []
    
    for role_name, profile in ROLE_PROFILES.items():
        profile_skills = profile["skills"]
        profile_skills_lower = {s.lower() for s in profile_skills}
        
        # Calculate intersection
        matching_skills = [s for s in profile_skills if s.lower() in user_skills_set]
        missing_skills = [s for s in profile_skills if s.lower() not in user_skills_set]
        
        # Calculate percentage match
        match_pct = 0.0
        if len(profile_skills) > 0:
            match_pct = (len(matching_skills) / len(profile_skills)) * 100
            
        recommendations.append({
            "role": role_name,
            "category": profile["category"],
            "description": profile["description"],
            "match_percentage": round(match_pct, 1),
            "matching_skills": sorted(matching_skills),
            "missing_skills": sorted(missing_skills),
            "insights": profile.get("insights", {})
        })
        
    # Sort recommendations by highest match percentage
    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    # 1. Primary predicted category & role based on top match
    top_recommendation = recommendations[0]
    predicted_category = top_recommendation["category"]
    predicted_role = top_recommendation["role"]
    category_confidence = top_recommendation["match_percentage"]
    
    # If the user has 0 matching skills anywhere, set fallback category
    if category_confidence == 0:
        predicted_category = "Software Engineering"
        predicted_role = "Junior Developer"
        category_confidence = 10.0
        
    # 2. Extract specific learning path recommendations for top 3 matching roles
    top_3_roles = recommendations[:3]
    learning_paths_dict = {}
    
    for rec in top_3_roles:
        role = rec["role"]
        missing = rec["missing_skills"]
        
        paths = []
        for skill in missing:
            skill_lower = skill.lower()
            if skill_lower in LEARNING_PATHWAYS:
                paths.append(LEARNING_PATHWAYS[skill_lower])
            else:
                # Default dynamic guidance if skill not explicitly mapped
                paths.append(f"📚 **{skill}**: Master this skill by reviewing official documentations, building a dedicated mini-project, and studying standard online tutorials.")
                
        # Limit to top 5 missing skills to avoid overwhelming the candidate
        learning_paths_dict[role] = paths[:5]
        
    # 3. Add a general category prediction message
    prediction_summary = f"Based on your skillset, your primary category is predicted as **{predicted_category}** (Confidence: {category_confidence}%). You show strong alignment for a **{predicted_role}** career pathway."
    
    return {
        "predicted_category": predicted_category,
        "predicted_role": predicted_role,
        "category_confidence": category_confidence,
        "prediction_summary": prediction_summary,
        "top_recommendations": top_3_roles,
        "learning_paths": learning_paths_dict
    }
