/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that might contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /* 
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        
        /* 
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'primary': '#3B82F6',    // Blue-500
                'primary-focus': '#2563EB',  // Blue-600
                'primary-content': '#FFFFFF',
                'secondary': '#10B981',  // Emerald-500
                'secondary-focus': '#059669',  // Emerald-600
                'secondary-content': '#FFFFFF',
                'accent': '#F59E0B',     // Amber-500
                'accent-focus': '#D97706',  // Amber-600
                'accent-content': '#FFFFFF',
                'neutral': '#374151',    // Gray-700
                'neutral-focus': '#1F2937',  // Gray-800
                'neutral-content': '#FFFFFF',
                'base-100': '#FFFFFF',
                'base-200': '#F9FAFB',   // Gray-50
                'base-300': '#F3F4F6',   // Gray-100
                'base-content': '#1F2937',  // Gray-800
                'info': '#3ABFF8',
                'success': '#36D399',
                'warning': '#FBBD23',
                'error': '#F87272',
            },
            fontFamily: {
                'sans': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
    daisyui: {
        themes: [
            {
                edumore: {
                    'primary': '#3B82F6',
                    'primary-focus': '#2563EB',
                    'primary-content': '#FFFFFF',
                    'secondary': '#10B981',
                    'secondary-focus': '#059669',
                    'secondary-content': '#FFFFFF',
                    'accent': '#F59E0B',
                    'accent-focus': '#D97706',
                    'accent-content': '#FFFFFF',
                    'neutral': '#374151',
                    'neutral-focus': '#1F2937',
                    'neutral-content': '#FFFFFF',
                    'base-100': '#FFFFFF',
                    'base-200': '#F9FAFB',
                    'base-300': '#F3F4F6',
                    'base-content': '#1F2937',
                    'info': '#3ABFF8',
                    'success': '#36D399',
                    'warning': '#FBBD23',
                    'error': '#F87272',
                },
            },
        ],
    },
}
