/**
 * User Storage Utility
 * Manages user registration and authentication using localStorage
 * Passwords are hashed using Web Crypto API (SHA-256)
 */

const USERS_KEY = 'app_users';

/**
 * Hash password using SHA-256
 */
async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

/**
 * Get all users from localStorage
 */
function getUsers() {
  try {
    const usersData = localStorage.getItem(USERS_KEY);
    return usersData ? JSON.parse(usersData) : {};
  } catch (error) {
    console.error('Error reading users:', error);
    return {};
  }
}

/**
 * Save users to localStorage
 */
function saveUsers(users) {
  try {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
    return true;
  } catch (error) {
    console.error('Error saving users:', error);
    return false;
  }
}

/**
 * Register a new user
 */
export async function registerUser(username, password) {
  if (!username || !password) {
    return { success: false, message: 'Username and password are required' };
  }

  if (username.length < 3) {
    return { success: false, message: 'Username must be at least 3 characters' };
  }

  if (password.length < 6) {
    return { success: false, message: 'Password must be at least 6 characters' };
  }

  const users = getUsers();

  // Check if user already exists
  if (users[username.toLowerCase()]) {
    return { success: false, message: 'Username already exists. Please login or choose a different username.' };
  }

  // Hash password
  const hashedPassword = await hashPassword(password);

  // Save user
  users[username.toLowerCase()] = {
    username: username,
    password: hashedPassword,
    createdAt: new Date().toISOString()
  };

  if (saveUsers(users)) {
    return { success: true, message: 'Account created successfully!' };
  } else {
    return { success: false, message: 'Failed to create account. Please try again.' };
  }
}

/**
 * Authenticate user
 */
export async function authenticateUser(username, password) {
  if (!username || !password) {
    return { success: false, message: 'Username and password are required' };
  }

  const users = getUsers();
  const user = users[username.toLowerCase()];

  if (!user) {
    return { success: false, message: 'Invalid username or password' };
  }

  // Hash provided password and compare
  const hashedPassword = await hashPassword(password);

  if (hashedPassword === user.password) {
    return { 
      success: true, 
      message: 'Login successful!',
      username: user.username 
    };
  } else {
    return { success: false, message: 'Invalid username or password' };
  }
}

/**
 * Check if user exists
 */
export function userExists(username) {
  const users = getUsers();
  return !!users[username.toLowerCase()];
}

/**
 * Get all registered usernames (for admin purposes)
 */
export function getAllUsernames() {
  const users = getUsers();
  return Object.values(users).map(u => u.username);
}

/**
 * Delete user (for testing purposes)
 */
export function deleteUser(username) {
  const users = getUsers();
  if (users[username.toLowerCase()]) {
    delete users[username.toLowerCase()];
    saveUsers(users);
    return true;
  }
  return false;
}

/**
 * Clear all users (for testing purposes)
 */
export function clearAllUsers() {
  localStorage.removeItem(USERS_KEY);
  return true;
}
