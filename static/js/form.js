document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('country');
    const citySelect = document.getElementById('city');
    
    // 获取国家列表
    fetch('/api/countries')
        .then(response => response.json())
        .then(data => {
            data.data.forEach(country => {
                const option = document.createElement('option');
                option.value = country.country;
                option.textContent = country.country;
                countrySelect.appendChild(option);
            });
        });

    // 当国家改变时获取城市列表
    countrySelect.addEventListener('change', function() {
        const country = this.value;
        citySelect.disabled = true;
        citySelect.innerHTML = '<option value="">Loading cities...</option>';

        if (country) {
            fetch('/api/cities', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ country: country })
            })
            .then(response => response.json())
            .then(data => {
                citySelect.innerHTML = '<option value="">Select a city</option>';
                if (data.data && Array.isArray(data.data)) {
                    data.data.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city;
                        option.textContent = city;
                        citySelect.appendChild(option);
                    });
                    citySelect.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                citySelect.innerHTML = '<option value="">Error loading cities</option>';
            });
        } else {
            citySelect.innerHTML = '<option value="">First select a country</option>';
        }
    });

    // 图片预览
    const photoInput = document.getElementById('photo');
    const previewDiv = document.getElementById('preview');
    
    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewDiv.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            };
            reader.readAsDataURL(file);
        }
    });
});