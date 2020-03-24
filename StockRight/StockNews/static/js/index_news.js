var api_value = JSON.parse('{{api}}');
console.log(api_value);
// function myfunction(){
//     $.ajax({
//         url: '{{api}}',
//         dataType: 'json',
//         type: 'get',
//         cache: false,
//         success: function(data){
//             $(data.data).each(function(index, value){
//                 console.log(data);
//                 var idx1 = "<li class=\"newsticker__item\"><a href='"+value.news_url+"'class=\"newsticker__item-url\">"+value.title+"</a></li>";
//                 $('#newsticker__list').append(idx1)
//             });
//         }
//     });
// }
// myfunction();