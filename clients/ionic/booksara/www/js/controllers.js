angular.module('starter.controllers', [])

.controller('DashCtrl', function($scope, $http, $state) {
  $scope.$on('$ionicView.enter', function(e){
    if (!token){
      back_to_login($scope, $state);
    }
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    $http.post(
      booksaraURL + 'api/q/generalstat/',
      'token=' + token
    ).success(function(data){
      $scope.book = data;
    }).error(function(){
      $scope.messag = 'error to reading from booksara stat';
      console.log("Error To Reading From Booksara State");
    })
  })
})

.controller('BooksCtrl', function($scope, $http, $state, $ionicModal, $ionicActionSheet) {
  // document.getElementById("uploadBtn").onchange = function () {
  //   document.getElementById("uploadFile").value = this.value;
  // };
  $scope.show = function() {

   // Show the action sheet
   var hideSheet = $ionicActionSheet.show({
     buttons: [
     ],
     destructiveText: 'Delete',
     titleText: 'Are You Sure?',
     cancelText: 'Cancel',
     cancel: function() {
          // add cancel code..
        },
     buttonClicked: function(index) {
       return true;
     }
   });

   // For example's sake, hide the sheet after two seconds
   $timeout(function() {
     hideSheet();
   }, 2000);

   };
  $ionicModal.fromTemplateUrl('book-edit-modal.html',{
    scope: $scope,
    animation: 'slide-in-left',
  }).then(function(modal){
    $scope.modal = modal;
  });

  $scope.openModal = function(){
    $scope.modal.show();
  };

  $scope.submitBookModal = function(){
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8;data:image/jpeg;base64';
    $http.post(
      booksaraURL + 'api/q/book/edit/',
      'token=' + token + '&name=' + $scope.editbook.name + '&price=' + $scope.editbook.price + '&description=' + $scope.editbook.description + "&picture=" + $scope.editbook.picture + "&id=" + $scope.editbook.pk
    ).success(function(data){
      $scope.modal.hide();
      $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8;data:image/jpeg;base64';
      $http.post(
        booksaraURL + 'api/q/book/',
        'token=' + token
      ).success(function(data){
        $scope.books = JSON.parse(data);
      }).error(function(){
        $scope.message = "error to reading data";
      })
    }).error(function(){
      $scope.message = "اشکال در ذخیره اطلاعات";
      console.log("error to save data");
    })
  };

  $scope.closeModal = function(){
    $scope.modal.hide();
  };

  $scope.$on('$destroy', function() {
    $scope.modal.remove();
  });
  // Execute action on hide modal
  $scope.$on('modal.hidden', function() {
    // Execute action
  });
  // Execute action on remove modal
  $scope.$on('modal.removed', function() {
  // Execute action
  });
  $scope.$on('$ionicView.enter', function(e) {
    if (!token) {
      back_to_login($scope, $state);
    }
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8;data:image/jpeg;base64';
    $http.post(booksaraURL + 'api/q/book/', 'token='+token).success(function(data) {
      $scope.books = JSON.parse(data);
    }).error(function() {
      $scope.message = 'erorr reading previous books' //TODO: show some error to user       console.log('error on request')
    })
  });

  $scope.shouldShowDelete = false;
  $scope.listCanSwipe = true;


  $scope.edit = function(item){
    $scope.modal_edit_name = item.fields.name;
    $scope.modal_edit_price = item.fields.price;
    $scope.modal_edit_description = item.fields.description;
    $scope.modal_edit_picture = item.fields.picture;
    $scope.modal_edit_pk = item.pk;
    $scope.editbook = {name: item.fields.name, price: item.fields.price, description: item.fields.description, picture: item.fields.picture, pk: item.pk};
    $scope.modal.show();
  }

  $scope.delete = function (item){
    console.log("delete Item Book : " + item.pk);
  }

  $scope.submit = function(){
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8;data:image/jpeg;base64';
    $http.post(
      booksaraURL + 'api/q/book/add/',
      'token=' + token + '&name=' + $scope.name + '&price=' + $scope.price + '&description=' + $scope.description + "&picture=" + $scope.picture + "&id=" + $scope.pk
    ).success(function(data){
      $scope.name = '';
      $scope.price = '';
      $scope.description = '';
      $scope.picture = '';
      $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8;data:image/jpeg;base64';
      $http.post(booksaraURL + 'api/q/book/', 'token=' + token).success(function(data) {
        $scope.books = JSON.parse(data);
      }).error(function() {
        $scope.message = 'erorr reading previous book' //TODO: show some error to user       console.log('error on request')
      })
    }).error(function() {
      $scope.message = 'خطا در ذخیره اطلاعات. بعدا دوباره تلاش کنید' //TODO: show some error to user
      console.log('error while submitting books');
    })
  }
})

.controller('BookDetailCtrl', function($scope, $stateParams, Books) {
  $scope.$on('$ionicView.enter', function(e) {
    if (!token) {
      back_to_login($scope, $state);
    }
  })
  $scope.book = Books.get($stateParams.bookId);
})

.controller('ConfigCtrl', function($scope, $state, $http, $ionicHistory, $ionicPopup, $timeout) {
  $scope.showAlert = function() {

               var alertPopup = $ionicPopup.alert({
                 title: 'Error On Login!',
                 template: '<b>Error Login Request</b>'
               });

               alertPopup.then(function(res) {
                 console.log('Error On Login');
               });
             };
  $scope.loggedin = false;
  $scope.tabTitle = "ورود";
  token = storage.getItem('token');
  if (token){
    $scope.loggedin = true;
    $scope.tabTitle = "تنظیمات";
  }
  $scope.login = function () {
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    $http.post(
      booksaraURL + 'accounts/login/',
      'username=' + $scope.username + '&password=' + $scope.password
    ).success(function(data) {
          if (data.result == 'ok') {
            token = data['token'];
            storage.setItem('token', token);
            $scope.loggedin = true;
            console.log('logged in with token:' + token);
            $ionicHistory.clearCache([$state.current.name]).then(function() {
              $ionicHistory.clearCache(['tab']).then(function() {
                $state.reload();
              })
            })

            } else {
              $scope.showAlert();



              // request was fine, but error on username / password
              // TODO: toast message about failed login
            }
          }).error(function() {
            // $scope.showAlert();
            console.log("Error On request Login");
          })
        }

      

      $scope.logout = function(){
        console.log('logout');
        storage.removeItem('token');
        $scope.loggedin = false;
        token = null;
        $ionicHistory.clearCache([$state.current.name]).then(function () {
          $ionicHistory.clearCache(['tab']).then(function() {
            $state.reload();
          })
        })
      }
    })

    .controller('TabsCtrl', function($scope, $http, $state, $ionicHistory, $rootScope) {
      token = storage.getItem('token');
      $rootScope.loggedin = (token != null);
    })

    .controller('NewsCtrl', function($scope, $http, $state, $ionicHistory) {
      $scope.$on('$ionicView.enter', function(e) {
        $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
        $http.post(
          booksaraURL + 'api/news/'
        ).success(function(data){
          $scope.news = JSON.parse(data);
        }).error(function(){
          $scope.message = "Error To Reading Data";
        })
      })
    });
