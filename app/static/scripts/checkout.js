function toPayment(event, user_id) {
    event.preventDefault();
    var form = document.getElementById("userDetails")
    var formData = new FormData(form);
    var user_dict = {};
    user_dict['first_name'] = formData.get('first_name');
    user_dict['last_name'] = formData.get('last_name');
    user_dict['phone'] = formData.get('phone');
    fetch(`api/users/${user_id}`, {
        method: "put",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user_dict)
      })
    var adrs_dict = {};
    if (formData.get('address2'))
        adrs_dict['address'] = formData.get('address1') + ' ' + formData.get('address2');
    else
        adrs_dict['address'] = formData.get('address1')
    adrs_dict['city'] = formData.get('city');
    if (formData.get('region'))
        adrs_dict['region'] = formData.get('region');
    adrs_dict['country'] = formData.get('country');
    adrs_dict['zip_code'] = formData.get('zip_code');
    fetch(`api/users/${user_id}/address`, {
        method: "put",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(adrs_dict)
      })
    document.getElementById("userDetails").classList.add("hidden");
    document.getElementById("paypal-button-container").classList.remove("hidden");
    document.getElementById('title').textContent = 'Payment Details'
}