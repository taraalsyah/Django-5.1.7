function confirmDelete() {
    return confirm("Are you sure you want to delete this item?");
};




$(document).ready(function () {
    $("#id_country").change(function () {
        var countryId = $(this).val();
        if (countryId) {
            $.ajax({
                url: ajaxLoadCitiesUrl, // namespace + view name
                data: { 'country_id': countryId },
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (data) {
                    $("#id_city").empty().append('<option value="">Choose</option>');
                    $.each(data, function (index, city) {
                        $("#id_city").append('<option value="' + city.id + '">' + city.name + '</option>');
                    });
                }
            });
        } else {
            $("#id_city").empty().append('<option value="">Choose</option>');
        }
    });
});
