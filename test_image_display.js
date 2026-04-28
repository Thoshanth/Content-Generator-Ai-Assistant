// Simple test to generate an image and check if it displays in chat
const API_BASE = 'http://localhost:8080/api';

async function testImageDisplay() {
    console.log('🖼️ Testing Image Display in Chat...\n');
    
    try {
        // Step 1: Register and login to get fresh token
        console.log('1️⃣ Registering new user...');
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
        
        console.log('✅ User registered successfully');
        
        // Step 2: Login
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
        
        // Step 3: Generate image
        console.log('\n3️⃣ Testing image generation...');
        const imageResponse = await fetch(`${API_BASE}/images/generate`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${loginData.accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: 'A cute cat sitting on a windowsill',
                style: 'realistic',
                width: 1024,
                height: 1024
            })
        });
        
        if (!imageResponse.ok) {
            const error = await imageResponse.text();
            console.log('❌ Image generation failed:', error);
            return;
        }
        
        const imageData = await imageResponse.json();
        console.log('✅ Image generation successful!');
        console.log('📝 Response data:', JSON.stringify(imageData, null, 2));
        
        // Step 4: Test image URL access
        if (imageData.imageUrl) {
            console.log('\n4️⃣ Testing image URL access...');
            console.log('🔗 Image URL:', `http://localhost:8080${imageData.imageUrl}`);
            
            const imageAccessResponse = await fetch(`http://localhost:8080${imageData.imageUrl}`, {
                method: 'HEAD',
                headers: {
                    'Authorization': `Bearer ${loginData.accessToken}`
                }
            });
            
            if (imageAccessResponse.ok) {
                console.log('✅ Image URL is accessible');
                console.log('📊 Content-Type:', imageAccessResponse.headers.get('content-type'));
                console.log('📏 Content-Length:', imageAccessResponse.headers.get('content-length'));
            } else {
                console.log('❌ Image URL not accessible:', imageAccessResponse.status, imageAccessResponse.statusText);
            }
        }
        
    } catch (error) {
        console.error('💥 Test failed with error:', error.message);
    }
}

// Run the test
testImageDisplay();