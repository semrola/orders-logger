(function() {

	var app = angular.module('orders', ['ngCookies']);

    //-------------SERVICES-------------------

    app.factory('Helper', ['$http', 'Properties', function($http, props) {
        this.confirm_goods = function(idValue, tip, shipping, ctrlarray) {    //received
            data = {};
            data[tip] = idValue;    //tip je item ali order
            if (shipping == 1) {
                data['shipping'] = 1;
            }
            $http.post('api/orders/confirm_order/',data, props.cookie)
            .then(function(response) {
                //success
                //poiscem objekt v orders z istim ID in mu posodobim polje received
                var order_to_update = ctrlarray.filter(function(obj) {
                    return obj.id === idValue;
                })[0];
                if(shipping == 1) {
                    order_to_update.shipped=response.data.shipped;
                } else {
                    order_to_update.received=response.data.received;
                }

            }, function() {});
        };
        return this;
    }]);

	app.factory('Properties', function() {
	    return {
		    static_path : '/static/orders/',
		    includes_path: 'includes/',
		    api_path: 'api/',
            cookie: {'xsrfHeaderName': 'X-CSRFToken', 'xsrfCookieName': 'csrftoken'},
	    };
	});

    //------------CONTROLLERS------------------

	app.controller('OrdersController', ['$http', 'Properties', 'Helper', function($http, props, helper) {
		var allOrders = this;

		$http.get('api/orders').then(function(data) {
			allOrders.orders = data.data;
		});



		this.shows = new Array();
		this.show = function(order) {
			if (!this.shows[order])
				this.shows[order] = true;
			else
				this.shows[order] = false;
		}

		this.confirm_goods = function(id, ship) {
		    return helper.confirm_goods(id, 'order', ship, allOrders.orders);
		}

	}]);

	app.controller('TabsController', ['$sce', '$cookies', 'Properties', function($sce, $cookies, props) {
	    var current = $cookies.get('tab');
	    if(!current) {
	        this.tab = 0;
        }
	    else {
	        this.tab = parseInt(current);
        }

		this.setTab = function(newtab) {
			this.tab = newtab;
			$cookies.put('tab', newtab);
		};
		var static = props.static_path + props.includes_path;

		this.tabObjects = [
		    {page: '<a>Homepage</a>', link: static + 'homepage.html'},
		    {page: '<a>New order</a>', link: static + 'neworder.html'},
		    {page: '<a>All orders</a>', link: static + 'allorders.html'},
		    {page: '<a>Latest orders</a>', link: static + 'latest.html'},
		    {page: '<a>Not received</a>', link: static + 'notreceived.html'},
		    {page: '<a>Stores</a>', link: static + 'stores.html'},
		];

	}]);

	app.controller('NewOrderController', ['$http', function($http) {
	    var neworderscon = this;

	    this.order = {};
	    this.items = [];

	    this.getStores = function() {
            $http.get('api/stores').then(function(data) {
                neworderscon.stores = data.data;
            });
        }

        this.getStores();

        this.addItem = function(){
            if(!this.item.differentfrom) {
                this.item.shfrom = this.order.shfrom
            }
            if(!this.item.differentto) {
                this.item.shto = this.order.shto
            }
            this.items.push(this.item);
            this.item = {}
        };
        this.removeItem = function(index){
            this.items.splice(index, 1);
        };

        this.submitOrder = function() {
            this.order.items = this.items;
            data = {order: this.order};
            $http.post('api/orders/new_order/',data,
		        {'xsrfHeaderName': 'X-CSRFToken', 'xsrfCookieName': 'csrftoken'})
		        .then(function() {
		           //success - strani z narocili morajo ponovno prenesti podatke
		        });
        };
	}]);

	app.controller('StoreController', ['$http','$scope', function($http, $scope) {
	    var storecontroller = this;

        var getstores = function() {
            $http.get('api/stores').then(function(data) {
                $scope.allstores = data.data;
            });
        }

        getstores();

        $scope.store = {};
	    $scope.submitStore = function() {
	        $http.post('api/stores/new_store/', $scope.store,
		        {'xsrfHeaderName': 'X-CSRFToken', 'xsrfCookieName': 'csrftoken'})
		        .then(function() {
		            //$scope.$apply();
		            getstores();
		            $scope.store = {};
                    //storecontroller.allstores.push(storecontroller.store);
		        });
	    };

	    $scope.removeStore = function(storeid, index) {
	        $http.post('api/stores/remove_store/', {id: storeid},
		        {'xsrfHeaderName': 'X-CSRFToken', 'xsrfCookieName': 'csrftoken'})
		        .then(function() {
                    getstores();
                    //storecontroller.allstores.splice(index, 1);
		        });
	    };

	    $scope.confirmEdit = function(store) {
	        $http.post('api/stores/edit_store/', store,
		        {'xsrfHeaderName': 'X-CSRFToken', 'xsrfCookieName': 'csrftoken'})
		        .then(function() {
                    getstores();
                    //storecontroller.allstores.splice(index, 1);
		        });
	    };
	}]);

    //------------DIRECTIVES-----------------------

	app.directive('items', function() {
		return {
			restrict: 'A',
			templateUrl: '/static/orders/includes/items.html',
			replace: true,
			bindToController: {
			    order: '=orderid'
			},
			controller:
			    ['$http', 'Properties', 'Helper', function($http, props, helper) {
                    var items = this;
                    var cached_items = new Array();
                    this.get_item = function(index) {
                        if(!cached_items[index]) {
                            $http.get('api/items/get_order/?order=' + this.order).then(function(response) {
                                items.all_items = response.data;
                                cached_items[index] = items.all_items;
                            }, function() {});
                        }
                        else {
                            items.all_items = cached_items[index];
                        };
                    };

                    this.confirm_items = function(id, ship) {
                        return helper.confirm_goods(id, 'item', ship, items.all_items);
                    };
                }],
			controllerAs: 'items_con'
		};
	});

    //----------FILTERS---------------------------

	app.filter('myDate', function($filter) {
		var angularDateFilter = $filter('date');
		var DATE_FORMAT = 'dd.MM.yyyy, H:MM';
		return function(theDate) {
		   return angularDateFilter(theDate, DATE_FORMAT);
		};
	});

	app.filter('myDateWHM', function($filter) {
		var angularDateFilter = $filter('date');
		var DATE_FORMAT = 'dd.MM.yyyy';
		return function(theDate) {
		   return angularDateFilter(theDate, DATE_FORMAT);
		};
	});

	app.filter('trustAsHtml', function ($sce) {
        return function (value) {
            return $sce.trustAsHtml(value);
        };
    });

    app.filter('getDateDiff', function() {
        return function(ordered, received, b) {
            // b - is received
            var date;
            if (b) {
                date = new Date(received) - new Date(ordered);
            }
            else
                date = new Date() - new Date(ordered);
            return Math.round(date/1000/60/60/24);
        };
    });

	/*
	app.filter('myCurrency', function() {
		var ngCurrencyFilter = $filter('currency');
		return function(amount) {
			mySimbol = '€'
			return ngCurrencyFilter(amount, mySimbol)
		};
	});*/

})();





