# Database Schema

This document describes the database schema and important data relationships for the Minimal Social Network project.

## Tables

### Users
- id: UUID (Primary Key)
- username: VARCHAR(50) (Unique)
- email: VARCHAR(100) (Unique)
- password_hash: VARCHAR(255)
- first_name: VARCHAR(50)
- last_name: VARCHAR(50)
- date_of_birth: DATE
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- avatar: VARCHAR(255)

### Posts
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key referencing Users.id)
- content: TEXT
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- like_count: INTEGER
- retweet_count: INTEGER
- original_post_id: UUID (Foreign Key referencing Posts.id, nullable)

### Connections
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key referencing Users.id)
- connected_user_id: UUID (Foreign Key referencing Users.id)
- status: ENUM('pending', 'accepted', 'rejected')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### Likes
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key referencing Users.id)
- post_id: UUID (Foreign Key referencing Posts.id)
- created_at: TIMESTAMP

### Comments
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key referencing Users.id)
- post_id: UUID (Foreign Key referencing Posts.id)
- content: TEXT
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### Messages
- id: UUID (Primary Key)
- sender_id: UUID (Foreign Key referencing Users.id)
- recipient_id: UUID (Foreign Key referencing Users.id)
- content: TEXT
- created_at: TIMESTAMP
- read_at: TIMESTAMP (nullable)

## Relationships

1. Users and Posts:
   - One-to-Many: A user can have multiple posts, but each post belongs to only one user.

2. Users and Connections:
   - Many-to-Many: Users can have multiple connections, and each connection involves two users.

3. Users and Likes:
   - One-to-Many: A user can like multiple posts, and a post can be liked by multiple users.

4. Users and Comments:
   - One-to-Many: A user can comment on multiple posts, and a post can have multiple comments from different users.

5. Posts and Likes:
   - One-to-Many: A post can have multiple likes, but each like is associated with only one post.

6. Posts and Comments:
   - One-to-Many: A post can have multiple comments, but each comment is associated with only one post.

7. Users and Messages:
   - One-to-Many: A user can send multiple messages, and a user can receive multiple messages.

## Indexes

To optimize query performance, consider adding indexes on:
- Users: username, email, first_name, last_name
- Posts: user_id, created_at, original_post_id
- Connections: user_id, connected_user_id, status
- Likes: user_id, post_id
- Comments: user_id, post_id, created_at
- Messages: sender_id, recipient_id, created_at

## Data Integrity

- Use foreign key constraints to ensure referential integrity between related tables.
- Implement cascading deletes where appropriate (e.g., deleting a post should delete all associated likes and comments).
- Use transactions for operations that involve multiple tables to ensure data consistency.

## Claude Engineer Optimizations

With the assistance of Claude Engineer, the following optimizations have been implemented:

1. Efficient indexing strategies for improved query performance
2. Optimized data relationships to minimize redundancy and improve data integrity
3. Suggestions for appropriate data types and constraints to ensure data consistency
4. Performance tuning recommendations for high-traffic tables

These optimizations contribute to a more scalable and efficient database structure, supporting the growing needs of the Minimal Social Network application.