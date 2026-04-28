// Test script to verify image generation authentication
const API_BASE = 'http://localhost:8080/api';

async function testImageAuth() {
    console.log('🧪 Testing Image Generation Authentication...\n');
    
    try {
        // Step 1: Register a test user
        console.log('1️⃣ Registering test user...');
        const testEmail = `test_${Date.now()}_${Math.random().toString(36).substr(2, 9)}@example.com`;
        const testUsername = `testuser_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
        
        const registerResponse = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: testEmail,
                username: testUsername,
                password: 'TestPassword123!',
                fullName: 'Test User'
            })
        });
        
        if (!registerResponse.ok) {
            const error = await registerResponse.text();
            console.log('❌ Registration failed:', error);
            return;
        }
        
        const registerData = await registerResponse.json();
        console.log('✅ User registered successfully');
        
        // Step 2: Login to get tokens
        console.log('\n2️⃣ Logging in...');
        const loginResponse = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: testEmail,
                password: 'TestPassword123!'
            })
        });
        
        if (!loginResponse.ok) {
            const error = await loginResponse.text();
            console.log('❌ Login failed:', error);
            return;
        }
        
        const loginData = await loginResponse.json();
        console.log('✅ Login successful');
        console.log('📝 Access Token:', loginData.accessToken ? 'Present' : 'Missing');
        
        // Step 3: Test debug endpoint (no auth required)
        console.log('\n3️⃣ Testing debug endpoint...');
        const debugResponse = await fetch(`${API_BASE}/images/debug-headers`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${loginData.accessToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        const debugData = await debugResponse.json();
        console.log('✅ Debug response:', debugData);
        
        // Step 4: Test auth endpoint (auth required)
        console.log('\n4️⃣ Testing auth endpoint...');
        const authTestResponse = await fetch(`${API_BASE}/images/test-auth`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${loginData.accessToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!authTestResponse.ok) {
            const error = await authTestResponse.text();
            console.log('❌ Auth test failed:', error);
            return;
        }
        
        const authTestData = await authTestResponse.json();
        console.log('✅ Auth test response:', authTestData);
        
        // Step 5: Test image generation
        console.log('\n5️⃣ Testing image generation...');
        const imageResponse = await fetch(`${API_BASE}/images/generate`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${loginData.accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: 'A beautiful sunset over mountains',
                style: 'realistic',
                width: 512,
                height: 512
            })
        });
        
        if (!imageResponse.ok) {
            const error = await imageResponse.text();
            console.log('❌ Image generation failed:', error);
            console.log('📊 Response status:', imageResponse.status);
            return;
        }
        
        const imageData = await imageResponse.json();
        console.log('✅ Image generation successful!');
        console.log('🖼️ Image URL:', imageData.imageUrl);
        console.log('🎨 Model used:', imageData.modelUsed);
        
        console.log('\n🎉 All tests passed! Authentication is working correctly.');
        
    } catch (error) {
        console.error('💥 Test failed with error:', error.message);
    }
}

// Run the test
testImageAuth();