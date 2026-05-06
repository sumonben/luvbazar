(function($) {

  "use strict";

  var initPreloader = function() {
    $(document).ready(function($) {
    var Body = $('body');
        Body.addClass('preloader-site');
    });
    $(window).load(function() {
        $('.preloader-wrapper').fadeOut();
        $('body').removeClass('preloader-site');
    });
  }

  // init Chocolat light box
	var initChocolat = function() {
		Chocolat(document.querySelectorAll('.image-link'), {
		  imageSize: 'contain',
		  loop: true,
		})
	}

  var initSwiper = function() {

    var swiper = new Swiper(".main-swiper", {
      speed: 500,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    var category_swiper = new Swiper(".category-carousel", {
      slidesPerView: 8,
      spaceBetween: 30,
      speed: 500,
      loop: false,
      navigation: {
        nextEl: ".category-carousel-next",
        prevEl: ".category-carousel-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
        991: {
          slidesPerView: 5,
        },
        1500: {
          slidesPerView: 8,
        },
      },
      on: {
        init: function() {
          updateCategoryCarouselButtons();
        },
        slideChange: function() {
          updateCategoryCarouselButtons();
        },
      }
    });

    // Function to update carousel button states
    function updateCategoryCarouselButtons() {
      const prevBtn = document.querySelector('.category-carousel-prev');
      const nextBtn = document.querySelector('.category-carousel-next');
      
      if (category_swiper.isBeginning) {
        prevBtn.classList.add('disabled');
        prevBtn.disabled = true;
      } else {
        prevBtn.classList.remove('disabled');
        prevBtn.disabled = false;
      }
      
      if (category_swiper.isEnd) {
        nextBtn.classList.add('disabled');
        nextBtn.disabled = true;
      } else {
        nextBtn.classList.remove('disabled');
        nextBtn.disabled = false;
      }
    }

    $(".products-carousel").each(function(){
      var $el_id = $(this).attr('id');

      var products_swiper = new Swiper("#"+$el_id+" .swiper", {
        slidesPerView: 5,
        spaceBetween: 30,
        speed: 500,
        navigation: {
          nextEl: "#"+$el_id+" .products-carousel-next",
          prevEl: "#"+$el_id+" .products-carousel-prev",
        },
        breakpoints: {
          0: {
            slidesPerView: 1,
          },
          768: {
            slidesPerView: 3,
          },
          991: {
            slidesPerView: 4,
          },
          1500: {
            slidesPerView: 5,
          },
        }
      });

    });

    // ========== Search Bar Functionality ==========
    const searchInput = document.getElementById('search-input');
    const searchForm = document.querySelector('.search-form');
    const searchContainer = document.querySelector('.search-container');
    const searchSuggestions = document.getElementById('search-suggestions');
    const searchCategory = document.getElementById('search-category');

    if (searchInput) {
      // Clear button functionality
      searchInput.addEventListener('input', function() {
        const clearBtn = this.parentElement.querySelector('.search-clear');
        if (clearBtn) {
          clearBtn.style.display = this.value ? 'flex' : 'none';
        }
      });

      // Search input focus effects
      searchInput.addEventListener('focus', function() {
        searchContainer.classList.add('focused');
      });

      searchInput.addEventListener('blur', function() {
        searchContainer.classList.remove('focused');
        // Hide suggestions after short delay to allow clicking
        setTimeout(() => {
          if (searchSuggestions) {
            searchSuggestions.style.display = 'none';
          }
        }, 200);
      });

      // Fetch search suggestions on input
      searchInput.addEventListener('input', async function(e) {
        const query = this.value.trim();
        
        if (query.length < 2) {
          if (searchSuggestions) {
            searchSuggestions.style.display = 'none';
          }
          return;
        }

        try {
          const response = await fetch(`/products/search-autocomplete/?q=${encodeURIComponent(query)}`, {
            headers: {
              'X-Requested-With': 'XMLHttpRequest'
            }
          });

          if (response.ok) {
            const data = await response.json();
            displaySearchSuggestions(data.results || []);
          }
        } catch (error) {
          console.log('Search suggestions not available');
        }
      });

      // Keyboard navigation in suggestions
      searchInput.addEventListener('keydown', function(e) {
        const items = searchSuggestions?.querySelectorAll('.search-suggestion-item');
        if (!items || items.length === 0) return;

        let selected = searchSuggestions?.querySelector('.selected');
        
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          if (!selected) {
            items[0].classList.add('selected');
          } else {
            const nextItem = selected.nextElementSibling;
            if (nextItem?.classList.contains('search-suggestion-item')) {
              selected.classList.remove('selected');
              nextItem.classList.add('selected');
              nextItem.scrollIntoView({ block: 'nearest' });
            }
          }
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          if (selected) {
            const prevItem = selected.previousElementSibling;
            if (prevItem?.classList.contains('search-suggestion-item')) {
              selected.classList.remove('selected');
              prevItem.classList.add('selected');
              prevItem.scrollIntoView({ block: 'nearest' });
            } else {
              selected.classList.remove('selected');
            }
          }
        } else if (e.key === 'Enter' && selected) {
          e.preventDefault();
          selected.click();
        }
      });
    }

    // Display search suggestions
    function displaySearchSuggestions(results) {
      if (!searchSuggestions) return;

      if (results.length === 0) {
        searchSuggestions.innerHTML = '<div style="padding: 16px; text-align: center; color: #999;">No products found</div>';
      } else {
        searchSuggestions.innerHTML = results.map(item => `
          <a href="${item.url}" class="search-suggestion-item" onclick="document.querySelector('.search-form').submit()">
            <svg class="search-suggestion-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"></path>
            </svg>
            <div>
              <div style="font-weight: 500; color: #333;">${escapeHtml(item.name)}</div>
              <div style="font-size: 0.85rem; color: #999;">${escapeHtml(item.category)}</div>
            </div>
          </a>
        `).join('');
      }

      searchSuggestions.style.display = 'block';
    }

    // Utility function to escape HTML
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // product single page
    var thumb_slider = new Swiper(".product-thumbnail-slider", {
      slidesPerView: 5,
      spaceBetween: 20,
      // autoplay: true,
      direction: "vertical",
      breakpoints: {
        0: {
          direction: "horizontal"
        },
        992: {
          direction: "vertical"
        },
      },
    });

    var large_slider = new Swiper(".product-large-slider", {
      slidesPerView: 1,
      // autoplay: true,
      spaceBetween: 0,
      effect: 'fade',
      thumbs: {
        swiper: thumb_slider,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });
  }

  // input spinner
  var initProductQty = function(){

    $('.product-qty').each(function(){
      
      var $el_product = $(this);
      var quantity = 0;
      
      $el_product.find('.quantity-right-plus').click(function(e){
        e.preventDefault();
        quantity = parseInt($el_product.find('#quantity').val());
        $el_product.find('#quantity').val(quantity + 1);
      });

      $el_product.find('.quantity-left-minus').click(function(e){
        e.preventDefault();
        quantity = parseInt($el_product.find('#quantity').val());
        if(quantity>0){
          $el_product.find('#quantity').val(quantity - 1);
        }
      });

    });

  }

  // init jarallax parallax
  var initJarallax = function() {
    jarallax(document.querySelectorAll(".jarallax"));

    jarallax(document.querySelectorAll(".jarallax-keep-img"), {
      keepImg: true,
    });
  }

  // document ready
  $(document).ready(function() {
    
    initPreloader();
    initSwiper();
    initProductQty();
    initJarallax();
    initChocolat();

  }); // End of a document

})(jQuery);