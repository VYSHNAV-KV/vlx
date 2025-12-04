document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_Categoryname');  // Replace with the correct field ID
    const additionalDataField = document.getElementById('id_additional_data');  // Replace with the correct field ID

    categorySelect.addEventListener('change', function () {
        const selectedCategory = categorySelect.value;

        if (selectedCategory === 'Electronics') {
            additionalDataField.placeholder = 'Enter technical specifications';
        } else if (selectedCategory === 'Clothing') {
            additionalDataField.placeholder = 'Enter fabric and size details';
        } else {
            additionalDataField.placeholder = 'Enter other product details';
        }
    });
});
