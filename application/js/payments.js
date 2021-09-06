var paymentdata;
const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  });

function sumTotals() {
    var sum = 0;
    $(".rentpay").each(function(){
        sum += +$(this).val();
    });
    $(".utilitiespay").each(function(){
        sum += +$(this).val();
    });
    $(".salestaxpay").each(function(){
        sum += +$(this).val();
    });
    $("#total").html(formatter.format(sum));
    var diff = $("#received").val() - sum;
    $("#remaining").html(formatter.format(diff));    
}

$(document).on("change", ".changes", function() {
    sumTotals();
});

$(document).on("click", "#save", function() {
    if($("#remaining").text() != 0) {
        alert("Input is not balanced");
    } else {
        $(".payrow").each(function( index ) {
            if($(".rent",this).prop("checked")) {
                var item = {};
                item.invoice = $(".invoice",this).text();
                item.salestax = $(".salestaxpay",this).val();
                item.rent = $(".rentpay",this).val();
                item.utilities = $(".utilitiespay",this).val();
                $.post(baseurl + "/payments/",item);
            }
            
          });
          location.reload();
    }
    
});

$(document).on("change", ".form-check-input", function() {
    if (this.checked) {
        var index = this.value;
        $('#row'+index + ' .rentpay').val(paymentdata[index].rentdue - paymentdata[index].rentpaid);
        $('#row'+index + ' .utilitiespay').val(paymentdata[index].utilitiesdue - paymentdata[index].utilitiespaid);
        $('#row'+index + ' .salestaxpay').val(paymentdata[index].salestaxdue - paymentdata[index].salestaxpaid);
    } else {
        var index = this.value;
        $('#row'+index + ' .rentpay').val(0);
        $('#row'+index + ' .utilitiespay').val(0);
        $('#row'+index + ' .salestaxpay').val(0);
    }
    sumTotals();
});



jQuery(function($) {

    let dropdown = $('#tenantSelect');
    dropdown.empty();
    dropdown.prop('selectedIndex', 0);
    const url = baseurl + '/tenants/';
    $.getJSON(url, function (data) {
    $.each(data, function (key, entry) {
        dropdown.append($('<option></option>').attr('value', entry.id).text(entry.name));
    })
    });

    let dropdown2 = $('#dateSelect');
    dropdown2.empty();
    dropdown2.prop('selectedIndex', 0);
    for(var i = 1; i <= 12; i++) {
        dropdown2.append($('<option></option>').attr('value', '2021-' + i + '-01').text(i + '/2021'));
    }
    

    $('#paymentModal').on('show.bs.modal', function (event) {

        
        let tenant = $('#tenantSelect').val();
        let date = $('#dateSelect').val();
        let invoiceurl = baseurl + '/invoices?tenant=' + tenant;
        const tenanturl = baseurl + '/tenants/' + tenant;
        let paymentBody = $('#paymentBody');
        paymentBody.empty();

        $.getJSON(invoiceurl, function (data) {
            paymentdata = data;
            $.each(data, function (key, entry) {
                if(entry.rentdue - entry.rentpaid > 0 || entry.utilitiesdue - entry.utilitiespaid > 0 || entry.salestaxdue - entry.salestaxpaid > 0) {
                    var $tr = $('<tr></tr>').attr('id', 'row' + key).attr('class','payrow').append(
                        $('<td>').append($('<input>').attr('class', 'form-check-input form-control rent changes').attr('value', key).attr('type', 'checkbox')),
                        $('<td>').text(entry.date),
                        $('<td>').text(entry.contract),
                        $('<td>').text(formatter.format(entry.rentdue)),
                        $('<td>').text(formatter.format(entry.rentdue - entry.rentpaid)),
                        $('<td>').append($('<input>').attr('class', 'form-control rentpay changes').attr('type', 'text').attr('value', 0)),
    
                        $('<td>').text(formatter.format(entry.utilitiesdue)),
                        $('<td>').text(formatter.format(entry.utilitiesdue - entry.utilitiespaid)),
                        $('<td>').append($('<input>').attr('class', 'form-control utilitiespay changes').attr('type', 'text').attr('value', 0)),
    
                        $('<td>').text(formatter.format(entry.salestaxdue)),
                        $('<td>').text(formatter.format(entry.salestaxdue - entry.salestaxpaid)),
                        $('<td>').append($('<input>').attr('class', 'form-control salestaxpay changes').attr('type', 'text').attr('value', 0)),

                        $('<td style="display:none;">').attr('class', 'invoice').text(entry.id)
                    );
                    paymentBody.append($tr);
                }
                
            })
        });
      })

    var $modal = $('#editor-modal'),
        $editor = $('#editor'),
        $editorTitle = $('#editor-title'),
        ft = FooTable.init('#editing-example', {
            "columns": $.get('static/paymentheaders.json'),
            "rows": $.get(baseurl + '/payments/'),
            editing: {
                enabled: true,
                addRow: function(){
                    $modal.removeData('row');
                    $editor[0].reset();
                    $editorTitle.text('Add a new row');
                    $modal.modal('show');
                },
                editRow: function(row){
                    var values = row.val();
                    console.log(values);
                    $editor.find('#id').val(values.id);
                    $editor.find('#contract').val(values.contract);
                    $editor.find('#rent').val(values.rent);
                    $editor.find('#utilities').val(values.utilities);
                    $editor.find('#salestax').val(values.salestax);
                    $editor.find('#paymentdate').val(values.paymentdate);
                    $modal.data('row', row);
                    $editorTitle.text('Edit row #' + values.id);
                    $modal.modal('show');
                },
                deleteRow: function(row){
                    if (confirm('Are you sure you want to delete the row?')){
                        $.ajax({
                            url: baseurl + "/payments/"+row.val().id + '/',
                            type: 'DELETE',
                            success: function(result) {
                                console.log("success");
                            }
                        });
                        row.delete();
                    }
                }
            }
        }),
        uid = 10;
  
    $editor.on('submit', function(e){
        if (this.checkValidity && !this.checkValidity()) return;
        e.preventDefault();
        var row = $modal.data('row'),
            values = {
                id: $editor.find('#id').val(),
                contract: $editor.find('#contract').val(),
                rent: $editor.find('#rent').val(),
                utilities: $editor.find('#utilities').val(),
                salestax: $editor.find('#salestax').val(),
                paymentdate: $editor.find('#paymentdate').val()
            };

        if (row instanceof FooTable.Row){
            
            var myData = {
                "id": values.id,
                "contract": values.contract,
                "rent": values.rent,
                "utilities": values.utilities,
                "salestax": values.salestax,
                "paymentdate": values.paymentdate
            };
            
            $.ajax({
                url: baseurl + "/payments/"+ values.id + '/',
                type: 'PATCH',
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(myData),
                success: function(result) {
                    console.log("success");
                }
            });
            
            row.val(values);
            
        } else {
            $.post(baseurl + "/payments/",{
				"id": values.id,
                "contract": values.contract,
                "rent": values.rent,
                "utilities": values.utilities,
                "salestax": values.salestax,
                "paymentdate": values.paymentdate
            });
            values.id = uid++;
            ft.rows.add(values);
        }
        $modal.modal('hide');
    });
 
});
