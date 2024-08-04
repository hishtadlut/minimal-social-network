# Database Schema

This document describes the database schema and important data relationships for the Minimal Social Network project.

## Tables

### Users
- id: UUID (Primary Key)
- username: VARCHAR(50) (Unique)
- email: VARCHAR(100) (Unique)
- password_hash: VARCHAR(255)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### Posts
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key referencing Users.id)
- content: TEXT
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

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

## Indexes

To optimize query performance, consider adding indexes on:
- Users: username, email
- Posts: user_id, created_at
- Connections: user_id, connected_user_id, status
- Likes: user_id, post_id
- Comments: user_id, post_id, created_at

## Data Integrity

- Use foreign key constraints to ensure referential integrity between related tables.
- Implement cascading deletes where appropriate (e.g., deleting a post should delete all associated likes and comments).
- Use transactions for operations that involve multiple tables to ensure data consistency.

This schema provides a foundation for the essential features of the Minimal Social Network. As the project evolves, you may need to add more tables or columns to support additional functionality.