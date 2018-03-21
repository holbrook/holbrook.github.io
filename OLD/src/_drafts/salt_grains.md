

# Using Grains in SLS modules
Often times a state will need to behave differently on different systems. Salt grains objects are made available in the template context. The grains can be used from within sls modules:

apache:
  pkg.installed:
    {% if grains['os'] == 'RedHat' %}
    - name: httpd
    {% elif grains['os'] == 'Ubuntu' %}
    - name: apache2
    {% endif %}